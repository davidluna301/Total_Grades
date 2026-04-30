#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py seed_db --grades
gunicorn evaluaciones_total_grades_estudiantes.wsgi:application