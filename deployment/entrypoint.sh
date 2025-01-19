#!/bin/bash

function usage() {
  echo "$0 <command> [params...]"
  echo "commands:"
  echo " - shell: runs django shell"
  echo " - bash: run container bash"
}

function debug() {
  if [ "$DEBUG" ]; then
    echo "DEBUG: $1"
  fi
}

 function django_run() {
  if which "$1"; then
    exec "$@"
  else
    exec ./blog/manage.py "$@"
  fi
}

if [ $# -eq 0 ]; then
  usage "$0"
  exit 1
fi

case $1 in
  "shell")
    debug "Starting django shell."
    django_run shell
    ;;
  "bash")
    debug "Starting bash."
    exec /bin/bash
    ;;
  "tests")
    debug "Running tests."
    DEBUG=1 exec "$(dirname "$0")/tests.sh"
    ;;
  *)
    echo "Invalid command: $1"
    usage "$0"
    exit 1
    ;;
esac

exit 1
