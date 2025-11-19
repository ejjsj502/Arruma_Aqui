#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

if [ -f "arruma/arruma/settings.py" ] && [ -f "arruma/settings.py" ]; then
    rm -rf arruma/arruma/
fi

python manage.py migrate
python manage.py collectstatic --noinput
echo "Build OK"
