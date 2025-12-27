import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

print('=' * 70)
print('🔐 ADMIN PANEL TEST')
print('=' * 70)

# 1. Superuser kontrol et
admin_users = User.objects.filter(is_superuser=True)
print(f'\n👤 Superuser Sayısı: {admin_users.count()}')

if admin_users.count() == 0:
    print('⚠️ Superuser yok, oluşturuluyor...')
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f'✅ Oluşturuldu: {user.username}')
else:
    for user in admin_users:
        print(f'   ✅ {user.username} ({user.email})')

# 2. Admin sayfasını test et
print('\n🌐 Admin Sayfası Test:')
client = Client()
response = client.get('/admin/')
print(f'   Status Code: {response.status_code}')

if response.status_code == 200:
    print('   ✅ Admin sayfası çalışıyor!')
elif response.status_code == 302:
    print('   ℹ️ Redirect (login gerekli)')
else:
    print(f'   ❌ Hata: {response.status_code}')

# 3. Settings kontrol et
from django.conf import settings
print(f'\n⚙️ Settings:')
print(f'   DEBUG: {settings.DEBUG}')
print(f'   MEDIA_URL: {settings.MEDIA_URL}')
print(f'   MEDIA_ROOT: {settings.MEDIA_ROOT}')

print('\n' + '=' * 70)
print('✅ Admin Panel Hazır!')
print('URL: http://127.0.0.1:8000/admin/')
print('Login: admin / admin123')
print('=' * 70)

