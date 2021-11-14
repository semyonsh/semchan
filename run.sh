#!/bin/bash
gunicorn3 -w 2 --bind 127.0.0.1:8081 --max-requests 500 wsgi:application
