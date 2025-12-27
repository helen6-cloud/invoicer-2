#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.api import Titles

print("=" * 70)
print("📊 TITLES DATABASE CHECK")
print("=" * 70)

# Toplam sayı
total = Titles.objects.count()
print(f"\n📌 Toplam başlık: {total}")

if total == 0:
    print("\n⚠️ Database'de veri yok!")
    print("Veri yüklemek için:")
    print("  1. data.json varsa: python manage.py loaddata data.json")
    print("  2. Yoksa: Django admin'den manuel ekle")
else:
    # Cesit'e göre ayırma
    filmler = Titles.objects.filter(cesit__icontains='film')
    diziler = Titles.objects.filter(cesit__icontains='dizi')

    print(f"\n🎬 Filmler: {filmler.count()}")
    for film in filmler[:3]:
        print(f"   - {film.title_name} ({film.yil})")

    print(f"\n📺 Diziler: {diziler.count()}")
    for dizi in diziler[:3]:
        print(f"   - {dizi.title_name} ({dizi.yil})")

    # Türü bilinmeyenler
    diger = Titles.objects.exclude(
        cesit__icontains='film'
    ).exclude(
        cesit__icontains='dizi'
    )
    if diger.count() > 0:
        print(f"\n❓ Diğer türler: {diger.count()}")
        for item in diger[:3]:
            print(f"   - {item.title_name} (Tür: {item.cesit})")

print("\n" + "=" * 70)

