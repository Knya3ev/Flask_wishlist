#!/bin/sh
source venv/bin/activate

if ! [-e "./app/wishlist.db"]; then
flask db init
flask db migrate

fi
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app

