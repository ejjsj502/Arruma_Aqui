#!/usr/bin/env bash
set -o errexit

echo "=== Instalando dependências ==="
pip install -r requirements.txt

echo "=== Verificando estrutura do projeto ==="
ls -la
find . -name "settings.py" -o -name "manage.py" | head -10

echo "=== Executando migrações ==="
python manage.py migrate

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Build concluído com sucesso ==="
