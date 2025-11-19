#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

if [ -f "arruma/arruma/settings.py" ] && [ -f "arruma/settings.py" ]; then
    rm -rf arruma/arruma/
fi

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

python manage.py migrate
python manage.py collectstatic --noinput
echo "✅ Build successful"
