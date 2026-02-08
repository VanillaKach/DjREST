#!/bin/bash
export $(grep -v "^#" .env | xargs)
python manage.py test --settings=DjREST.settings

