import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Eski admin'i sil
User.objects.filter(username='admin').delete()

# Yeni admin oluştur
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

print("✅ Superuser oluşturuldu!")
print("Username: admin")
print("Password: admin123")

