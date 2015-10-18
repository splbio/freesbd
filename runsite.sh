#!/bin/sh

echo "Starting up..."
. env/bin/activate && python website/site.py "$@"

