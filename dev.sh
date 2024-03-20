#!/bin/bash

# set -e
set -o pipefail

self_path=$(dirname "$0")
self=$(basename "$0")

cd "$self_path"

function elog { printf '%s\n' "$self: $*" >&2; }
function log { printf '%s\n' "$self: $*"; }

function trap_exit {
  if [[ -n "$killed" ]]; then exit; fi
  sleep 1.5
  echo
  elog killing processes
  if [[ -n "$postgrest_pid" ]]; then kill "$postgrest_pid"; fi
  if [[ -n "$backend_pid" ]]; then kill "$backend_pid"; fi
  if [[ -n "$frontend_pid" ]]; then kill "$frontend_pid"; fi
  killed=1

  # to pile onto the broken mindset of javascript developers, create-react-app
  # has also decided that, yes, this fucking ~~enhanced log viewer~~ needs to
  # set application keypad too; which of course mucks up the terminal when it
  # is killed, so fixed this garbage too. ffs.
  printf '\x1b>'
  exit
}

trap "trap_exit" INT KILL QUIT EXIT ERR


function try_enter_venv {
  for path in backend/.venva backend/.env backend/venv backend/env; do
    if [[ -d "$path" ]]; then
      if [[ -f "$path/bin/activate" ]]; then
        elog entering virtual environment $path
        source "$path/bin/activate"
        return
      elif [[ -f "$path/Scripts/activate" ]]; then
        elog entering virtual environment $path
        source "$path/bin/activate"
        return
      fi
    fi
  done

  elog not in a virtual environment and could not find one, exiting
  killed=1
  exit
}


if [[ -z "$VIRTUAL_ENV" ]]; then
  try_enter_venv
fi

log checking for migrations
log \$ backend-migrate
backend-migrate 2>&1 | sed 's/^\(.*\)$/\x1b\[95m\1\x1b\[39m/'

if [[ -z "$NO_NPM" ]]; then
  log updating npm
  cd frontend
  log \$ npm install --include=dev
  npm install --include=dev 2>&1 | sed 's/^\(.*\)$/\x1b\[91m\1\x1b\[39m/'
  cd ..
fi

echo
if [[ -e "backend/postgrest.conf" ]]; then
  postgrest_cfg="backend/postgrest.conf"
else
  postgrest_cfg="backend/postgrest.default.conf"
fi
log starting postgrest
log \$ postgrest $postgrest_cfg
postgrest "$postgrest_cfg" 2>&1 | sed 's/^\(.*\)$/\x1b\[92m\1\x1b\[39m/'&
postgrest_pid=$!

echo
log starting backend
log \$ backend
backend 2>&1 | sed 's/^\(.*\)$/\x1b\[95m\1\x1b\[39m/' &
backend_pid=$!

echo
log starting frontend dev
# create-react-app's npm scripts fucking clears the terminal with no intended
# toggle to disable, so fucking disable the CSI clear sequence for that process.
# in addition, for whatever fucking reason someone had the bright idea to launch
# the system browser, so shut that the fuck down (at least they put in a toggle)
cd frontend/
log \$ npm run start
PORT=8081 BROWSER=none npm run start 2>&1 \
  | sed -e 's/\x1b\[:digit:J//' -e 's/^\(.*\)$/\x1b\[91m\1\x1b\[39m/' &
frontend_pid=$!
cd ..
echo


wait "$postgrest_pid"
wait "$backend_pid"
wait "$frontend_pid"
