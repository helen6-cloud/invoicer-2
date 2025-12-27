import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

# Migration oluştur
print("📝 Migration oluşturuluyor...")
call_command('makemigrations')

# Migration'ları uygula
print("⚙️ Migration'lar uygulanıyor...")
call_command('migrate')

print("✅ Tamamlandı!")

