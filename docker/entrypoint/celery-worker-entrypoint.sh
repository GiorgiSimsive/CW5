#!/usr/bin/env bash
set -e
/app/docker/wait-for-it.sh db:5432 -t 60 -- echo "db ok"
/app/docker/wait-for-it.sh redis:6379 -t 60 -- echo "redis ok"
celery -A config worker -l info -c 2
