#!/usr/bin/env bash
set -o errexit

echo "=== Instalando Pillow primeiro ==="
pip install --upgrade pip
pip install Pillow==10.1.0 --no-binary=:all: || pip install Pillow==9.5.0

echo "=== Instalando outras dependências ==="
pip install -r requirements.txt

if [ -f "arruma/arruma/settings.py" ] && [ -f "arruma/settings.py" ]; then
    rm -rf arruma/arruma/
fi

python manage.py migrate
python manage.py collectstatic --noinput
echo "✅ Build com Pillow successful"
