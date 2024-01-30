# backend

## Configuing pip
To setup development environment, follow these steps:

1. Setup the virtual environment:
```bash
cd backend
virtualenv .venv
source .venv/bin/activate
```

2. Install the project and it's dependencies:
```bash
pip install -e .
```

Note: this pip project installs binaries! You should have `~/.local/bin` available on your path for them to work.

## Server Configuration
Generate the server configuration by running:
```bash
backend-setupcfg
```
This creates the file [`config.toml`](./config.toml) in the pip project directory. Edit this file in-place of [`config.default.toml`](./config.default.toml); values in `config.toml` will override those defined in `config.default.toml`.

This script will randomly generate a jwt_secret for your use.

Set the parameters in the `[ollama]` section to point to a running [ollama](https://ollama.ai/) API server.


## Installing & Configuring Postgres
To setup postgres, on any platform but windows, install the appropriate package:
- Homebrew: `brew install postgresql`
- Debian/Ubuntu based: `apt install postgresql`

On Windows, Docker should work, but your mileage may vary:
```bash
docker run --name tutorial -p 5433:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

On first install, setup a new user with a password and a database for them:
```bash
sudo -u postgres createuser -P $USERNAME
sudo -u postgres createdb -O $USERNAME public
```

Edit [`config.toml`](./config.toml) and change the fields under the `[db]` section to include the username, and database set above. If you installed postgres from a package and it is using a domain socket, change the `host` field to the directory containing the socket.


<!-- todo: finish this -->

## Running the Server

Run the main server entrypoint
```bash
python src/backend/main.py
```


<!-- todo: setup local database?? -->
