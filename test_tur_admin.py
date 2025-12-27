import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from backend.api import Tur

print("=" * 70)
print("🔍 TUR ADMIN SAYFASI TEST")
print("=" * 70)

# 1. Tur modeli kontrol et
print("\n1️⃣ Tur Modeli:")
print(f"   Toplam Tur: {Tur.objects.count()}")

for tur in Tur.objects.all()[:5]:
    print(f"   - {tur}")

# 2. Admin sayfasını test et
print("\n2️⃣ Admin Sayfası Test:")
client = Client()

# Login yap
client.login(username='admin', password='admin123')

# Tur admin sayfasına eriş
response = client.get('/admin/api/tur/')
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("   ✅ Sayfaya erişim sağlandı!")
elif response.status_code == 404:
    print("   ❌ Sayfa bulunamadı (404)")
    print("   Deneniyor: /admin/api/tur/")

    # Alternatif URL'leri dene
    urls = [
        '/admin/api/tur/',
        '/admin/tur/',
        '/admin/api/Tur/',
        '/admin/Tur/',
    ]

    for url in urls:
        resp = client.get(url)
        print(f"   {url}: {resp.status_code}")
else:
    print(f"   ⚠️ Hata: {response.status_code}")

# 3. Admin site'ın registered models'ını kontrol et
print("\n3️⃣ Registered Models:")
from django.contrib import admin as django_admin

for model, admin_class in django_admin.site._registry.items():
    if 'tur' in model.__name__.lower():
        print(f"   ✅ {model.__name__} registered")

print("\n" + "=" * 70)

