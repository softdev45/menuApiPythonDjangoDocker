#!/bin/bash
celery -A eMenu worker --loglevel=Info &
celery -A eMenu beat --loglevel=Info &
wait -n
exit $?

