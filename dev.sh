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

if [[ -z "$VIRTUAL_ENV" ]]; then
  elog not in a virtual environment, exiting
  killed=1
  exit
fi

log checking for migrations
log \$ backend-migrate
backend-migrate 2>&1 | sed 's/^\(.*\)$/\x1b\[95m\1\x1b\[39m/'

if [[ -z "$NO_NPM" ]]; then
log updating npm
log \$ npm install --include=dev --prefix frontend/
npm install --include=dev --prefix frontend/ 2>&1 | sed 's/^\(.*\)$/\x1b\[91m\1\x1b\[39m/'

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
log \$ npm run --prefix frontend/ start
PORT=8081 BROWSER=none npm run --prefix frontend/ start 2>&1 \
  | sed -e 's/\x1b\[:digit:J//' -e 's/^\(.*\)$/\x1b\[91m\1\x1b\[39m/' &
frontend_pid=$!
echo


wait "$postgrest_pid"
wait "$backend_pid"
wait "$frontend_pid"
