#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

celery -A poetriumph worker --loglevel=info --concurrency 1 -E
