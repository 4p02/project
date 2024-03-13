# Architecture

This document describes the architecture of our project which consists of three main services: the main Python FastAPI server nicknamed **backend**, a **postgrest** HTTP API gateway for accessing all database tables over HTTP, and **Ollama** that acts similar to an ClosedAI-like API. These three components are all interconnected to and within **backend**.


## Components

### backend
**backend**: Serves the main application endpoints with the help of FastAPI's framework. It is in charge of:

- Providing primary HTTP service entry points
- Handling user authentication & authorization through the `/auth/login` and `/auth/register` endpoints. They issue [JWT tokens](https://en.wikipedia.org/wiki/JSON_Web_Token) necessary to consume services like postgrest, or to use some authenticated backend endpoints.
- Handles oauth authentication through our oauth providers.
- Managing database table structure with the migrations present in `db/`.
- Proxying and queueing requests from the /shorten and /summarize endpoints sending requests to Ollama.

backend dependencies:
- **fastapi**: A web framework used for handling the main API. In turn, fastapi also requires a server to run it on (**unicorn**), and it heavily relies on **starlette** which is a lower-level framework. FastAPI feels the impulsive need to weld on actual garbage to starlette, quickly divorcing itself from starlette's designs, handling logging so ass-backwards that it's shocking how it can fuck up such a simple thing, and making most middleware from starlette nearly useless. But at least it has a documentation generator so yay?
- **starlette**: A web framework for making asynchronous APIs, and is used internally by fastapi. This framework (unlike the raging trash fire that is fastapi), starlette is actually well designed and pleasurable to use.
- **uvicorn**: A small ASGI server for running the FastAPI and starlette server.
- **jwt**: A Python implementation of JWT tokens, which we use for authentication.
- **typeguard**: A runtime type annotation checker, primarily used to type-check our configuration files.
- **psycopg**: A postgres adapter that provides connections, cursors, and transactions for our postgres database. This directly accesses the postgres database, bypasses any limitations of postgrest (with the "t"). This dependency requires libpq. A binary version is installed for Windows, since libpq is not readily available on there.
- **ollama**: A HTTP REST API for LLM chat completion, used for our summarization features.
- **authlib**: Implements OAuth support for third-party authentication.
- **itsdangerous**: Stub.
- **bcrypt**: A Python implementation of the Blowfish password hash algorithm (bcrypt), which provides password hashing and salting for secure storage of passwords in a standard format.
- **pytest**: Stub.


### postgrest
**postgrest**: Offers a flexible way to access postgrest database tables over an HTTP REST API. It handles and takes advantage of:
- Querying tables with `select`, `insert`, `update`, and `delete` queries over HTTP.
- Allowing downloading or uploading binary table fields as files (e.g. documents or images).
- Users are authenticated via JWT tokens issued by backend. The JWT token specifics which role is impersonated, presently it defaults to `pgrest_auth`.
- Anonymous access is allowed when a token isn't provided, with instead using the `pgrest_anon` role to control coarse table access.
- Row-level security policies which defines which rows a given role is allowed to access.
- All tables not present in the `public` schema (e.g. in the `private` schema) are completely off-limits to postgrest.

It obviously depends on the **postgres** database running, which is the main database engine we use:
- It supports the standard SQL language you're used to, with a few caveats about certain type names (e.g. use `text` for strings, `bytea` for binary text)
- It has a concept of users and roles. The user is what you specify in the connection string and is how you authenticate. The role specifics additional table or row permissions on top of your user permissions. Roles can be switched to and from while in a postgres session (this is the main feature that makes postgrest work).
- We configure our tables so that only specific tables and rows can be accessed by a given role with `grant` clauses that specify which of the primitive operations (`select`, `insert`, `update`, and `delete`) can be performed and on which columns can be affected by those queries
- In addition to `grant` clauses, we also set row-level security which constrains which rows a user or role is able to view and change. Note that row-level security, as the name implies, only allows changing which rows are visible to the current user/role, and it cannot constrain columns (use `grant` clauses, or custom views for that).

Both of these services are installed and configured in the setup instructions.


### Ollama
**Ollama**: Provides an HTTP REST API similar to that of ClosedAI's API. It's primary purpose is to perform chat completions on a selected model.

### Ancillary
**Apache**: A HTTP server that blends all our services together on production, and serves them alongside frontend. It is responsible for acting as the main HTTP gateway, and internally rerouting requests to the appropriate service, based on the subdomain and HTTP request path.

**systemd**: Our service manager on production, which is responsible for running all the aforementioned services, in the correct order. It also handles and classifies logging in production from all the services it managers, supports setting log verbosity levels, and exposes an easy management interface for parsing and searching log files. Services are restarted when the server restarts, the server is updated, or if it ever happens that any service crashes.


## Directory Structure

- `.venv/`: A virtual environment directory which separates our project's pip packages from system packages, which avoids some awful dependency hell that often arises with pip. This directory is generated when following the setup instructions.
- `ARCHITECTURE.md`: This file, that you are currently reading, serves as an overview and explanation of the project's architecture.
- `config.default.toml`: Stores various server settings. This file, `config.default.toml` is a default template that is checked into git and *should not contain any important secrets*.
- `config.toml`: This file, if present, will be loaded instead of `config.default.toml`, and it contains local configuration including secrets. It is autogenerated whenever `backend-setupcfg` is ran.
- `db/`: This directory contains SQL files for database migrations: for setting up postgres, initializing tables, row-level security, and mock data. These files are loaded in lexicographical order by the `backend-migrate` command. The currently indexed migration is set in the config under the key `db.current_migration` and is updated whenever a migration is ran.
- `postgrest.conf` and `postgrest.default.conf`: The `postgrest.conf` and `postgrest.default.conf` files are configuration files for postgrest. `postgrest.conf` is autogenerated whenever `backend-setupcfg` is ran.
- `pyproject.toml`: A configuration file for pip, specifying metadata, dependencies, and installed commands.
- `README.md`: Provides brief installation and setup instructions.
- `src/backend/`: The `src/backend/` directory contains code for main pip package of the backend application. It includes various modules and scripts that implement different functionalities, such as authentication, database management, API routing, data processing, etc.
  - `__init__.py`: Init file to make this folder a module, and offers some important globals for configuration and logging.
  - `auth.py`: This module handles user authentication through the `/auth/login` and `/auth/register` endpoints, and generating or parsing JWT tokens.
  - `cfg.py`: This module parses the `config.toml` configurations and defines the configuration schema and types.
  - `cli.py`: Contains command line interface scripts for running: `backend-migrate` which performs database migrations, and `backend-setupcfg` that generates local configuration files.
  - `db.py`: This module provides database-related functions and classes for interacting with the underlying PostgreSQL database, such as creating connections or executing SQL queries.
  - `main.py`: The main entry point of the backend server that initializes necessary components such connecting to the database and ollama servers, then starts running the HTTP server.
  - `misc.py`: This module contains shared miscellaneous utility functions that aren't specific to a particular module.
  - `models.py`: Classes representing database tables and FastAPI data models used as a data structures to handle data in a sane way.
  - `ollama.py`: Contains the Ollama server API and functions to perform chat completions.
  - `routes.py`: This module defines all our FastAPI routes for handling HTTP requests and returning responses, including endpoints for authentication and summarization. Endpoints for other tables are available through postgrest.
  - `shorten.py`: Stub.
  - `summarize.py`: Stub.
  - `test_routes.py`: Stub.
  - `yt_transcribe.py`: This module contains code for downloading YouTube video transcriptions.
- `TODO.md`: Shared todo list for immediate tasks that may or may not have a respective issue.
