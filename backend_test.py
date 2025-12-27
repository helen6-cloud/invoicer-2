#!/usr/bin/env python
"""
Backend test script - Kontrol et ve çalıştır
"""
import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from backend.api import Titles

print("=" * 60)
print("🔧 Backend Test Script")
print("=" * 60)

# 1. Migration kontrol et
print("\n✅ Step 1: Database migration'larını uygula...")
try:
    call_command('migrate')
    print("✅ Migration'lar başarıyla uygulandı!")
except Exception as e:
    print(f"❌ Migration hatası: {e}")
    sys.exit(1)

# 2. Database bağlantısı test et
print("\n✅ Step 2: Database bağlantısını test et...")
try:
    count = Titles.objects.count()
    print(f"✅ Database bağlantısı OK! Toplam başlık: {count}")
except Exception as e:
    print(f"❌ Database hatası: {e}")
    sys.exit(1)

# 3. Static files kontrol et
print("\n✅ Step 3: Static files'ları kontrol et...")
try:
    call_command('collectstatic', '--noinput')
    print("✅ Static files başarıyla taşındı!")
except Exception as e:
    print(f"⚠️ Static files hatası (önemli değil): {e}")

# 4. Sistem check
print("\n✅ Step 4: Django sistem kontrolü...")
try:
    call_command('check')
    print("✅ Django sistem kontrolü geçti!")
except Exception as e:
    print(f"❌ Sistem hatası: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TÜM TESTLER BAŞARILI!")
print("=" * 60)
print("\n🚀 Backend hazır! Şimdi çalıştırabilirsin:")
print("   python manage.py runserver")
print("\n📊 Verileri yüklemek için:")
print("   python manage.py load_custom_data")
print("   python manage.py fetch_tmdb_data --api_key YOUR_KEY")
print("=" * 60)

