#!/usr/bin/env bash
set -e
HP="$1"; shift
HOST="${HP%:*}"; PORT="${HP#*:}"
TIMEOUT=60
if [ "${1:-}" = "-t" ]; then TIMEOUT="$2"; shift 2; fi
if [ "${1:-}" = "--" ]; then shift; fi
for i in $(seq "$TIMEOUT"); do
  if nc -z "$HOST" "$PORT" >/dev/null 2>&1; then
    echo "$HOST:$PORT is up"
    exec "$@"
  fi
  sleep 1
done
echo "Timeout waiting for $HOST:$PORT" >&2
exit 1
