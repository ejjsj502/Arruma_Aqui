#!/usr/bin/env bash
set -o errexit

echo "=== Instalando dependências ==="
pip install -r requirements.txt

echo "=== Corrigindo estrutura duplicada ==="
if [ -f "arruma/arruma/settings.py" ] && [ -f "arruma/settings.py" ]; then
    rm -rf arruma/arruma/
fi

echo "=== Executando migrações ==="
python manage.py makemigrations  # ← ADICIONE ESTA LINHA
python manage.py migrate

echo "=== Criando superuser ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✅ Superuser criado: usuario=admin, senha=admin')
else:
    print('✅ Superuser já existe')
"

echo "=== Coletando arquivos estáticas ==="
python manage.py collectstatic --noinput

echo "✅ Build successful - Superuser: admin/admin"
