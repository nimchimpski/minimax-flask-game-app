#!/bin/bash
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
