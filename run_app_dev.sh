#!/bin/bash
# python manage.py db upgrade
sh migrate.sh | flask run --host=0.0.0.0 --port=$FLASK_PORT
