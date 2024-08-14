#!/bin/bash

export FAILED=0

function failed() {
  echo "FAILED: $1" >&2
  export FAILED=$((FAILED + 1))
}

function succeed() {
  echo "SUCCESS: $1"
}

function shell_check() {
  if ! which shellcheck; then
    echo shellcheck not found, ignoring >&2
  else
    test_path=$(dirname "${BASH_SOURCE[0]}")
    for s in "$test_path"/*.sh; do
      if shellcheck "$s"; then
        succeed "shellcheck: $s"
      else
        failed "shellcheck: $s > Failed with exit code $?"
      fi
    done;
  fi
}

# Usage tests
function test_usage() {
  if $ENTRYPOINT; then
    failed "usage: non errored exit"
  else
    succeed "usage"
  fi
}

# Shell test
function test_shell() {
  if ! result=$(echo "print(\"SUCCESS\");exit()" | $ENTRYPOINT shell); then
    failed "shell: Errored with non 0 exit code"
  elif [[ $result != *SUCCESS ]]; then
    failed "shell: Didn't output the expected result"
    echo "$result"
  else
    succeed "shell"
  fi
}

# Bash test
function test_bash() {
  if ! result=$(echo "echo SUCCESS && exit" | $ENTRYPOINT bash); then
    failed "bash: Errored with non 0 exit code"
  elif [[ $result != *SUCCESS ]]; then
    failed "bash: Didn't output the expected result"
    echo "$result"
  else
    succeed "bash"
  fi
}

# Run tests
echo "Running tests..."
echo "ENTRYPOINT=$ENTRYPOINT"

shell_check
test_usage
test_shell
test_bash
echo "Finished tests..."

if [ $FAILED -gt 0 ]; then
  echo "Tests failed." >&2
  exit 1
fi
echo "All tests passed"
exit 0
