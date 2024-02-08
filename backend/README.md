# backend

## Configuing pip
To setup development environment, follow these steps:

1. Ensure you have python 3.10, pip, and virtualenv installed and on your path.
If using Windows or if virtualenv is not installed with python, first check if there is a separate `virtualenv` package offered by your system. If not, run `pip install virtualenv` and in the following commands, subsitute `virtualenv` with `python -m virtualenv`.

2. Ensure your system path is configured properly.

This pip project installs binaries/scripts. You should have the following directory available on your path:
- `~/.local/bin` (on unix)
- `C:\Program Files\Python3\Scripts\` or `%appdata%\Python3\Scripts\` (on windows, depending on if python was installed system-wide or only for the current user)

You may need to manually add the directory to your path if it's not already added. On unix, the easiest way is to add `PATH="$(realpath -m ~/.local/bin):$PATH"` to your `.bashrc`, `.zshrc`, or `.profile`. On windows, rerun the python installer and check "Add Python to PATH", or [manually add the PATH entries](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path).

3. [Setup the virtual environment](https://virtualenv.pypa.io/en/latest/user_guide.html):
```bash
cd backend
virtualenv .venv
```

4. Enter the virtual environment. You will need to enter the virtual environment once every time you start a new shell/terminal session before running any `pip` commands or any project binaries.

If using bash or git bash (on windows):
```bash
source .venv/bin/activate
```

If using powershell (on windows):
```ps
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\.venv\Scripts\activate
```

5. Install the project, it's dependencies, and the binaries the project installs:
```bash
pip install -e .
```


## Server Configuration
Generate the server configuration by running:
```bash
backend-setupcfg
```
This creates the file [`config.toml`](./config.toml) in the pip project directory. Edit this file instead of [`config.default.toml`](./config.default.toml); values in `config.toml` will override those defined in `config.default.toml`.

- Set the parameters in the `[ollama]` section to point to a running [ollama](https://ollama.ai/) API server.
- This script will also randomly generate a jwt_secret for your use.


## Installing & Configuring Postgres
To setup postgres, on any platform but windows, install the appropriate package:
- Homebrew: `brew install postgresql`
- Debian/Ubuntu based: `apt install postgresql`

On Windows, Docker can run postgres. Alternatively, you can use the [postgres windows installer](https://www.postgresql.org/download/windows/), but your mileage may vary.
```bash
docker run --name postgres -p 5433:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

On first install, setup a new user with a password and a database for them:
```bash
sudo -u postgres createuser -P $USERNAME
sudo -u postgres createdb -O $USERNAME public
```

Edit [`config.toml`](./config.toml) and change the fields under the `[db]` section to include the username, and database set above. If you installed postgres from a package and it is using a domain socket, change the `host` field to the directory containing the socket.

## Running the Server

Run the main server entrypoint
```bash
python src/backend/main.py
```
## Setup oauth

Find the `/etc/hosts` file on the system and add the following line:
`127.0.0.1 simplify.com`

Then email jonathan to add ur gmail to the google oauth client list and for the client secret, (the one is an example)

## Fast API docs

Go to the url `http://127.0.0.1:8080/docs` to see the fast api documentation