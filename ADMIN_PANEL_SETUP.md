# ✅ Admin Panel Kurulumu Tamamlandı!

## 🎉 Admin Panel'e Girmek İçin:

### 📍 **URL:**
```
http://127.0.0.1:8000/admin/
```

### 👤 **Login Bilgileri:**
```
Username: admin
Password: admin123
```

---

## 🚀 **Adım Adım:**

### 1️⃣ Django Sunucusunu Başlat
```bash
python manage.py runserver
```

Çıktıda görmen gerekir:
```
Starting development server at http://127.0.0.1:8000/
```

### 2️⃣ Tarayıcıda Admin Paneline Git
```
http://127.0.0.1:8000/admin/
```

### 3️⃣ Login Yap
- **Username:** `admin`
- **Password:** `admin123`

### 4️⃣ "Başlıklar (Filmler/Diziler)" Bölümüne Tıkla

### 5️⃣ Yeni Başlık Ekle
**"+ ADD TITLE"** butonuna tıkla ve doldur:

| Alan | Örnek |
|------|-------|
| **Title name** | Inception |
| **Cesit** | Film |
| **Ozet** | Rüya dünyasında yolculuk |
| **Yil** | 2010 |
| **Sure** | 148 |
| **Poster resmi** | 📷 [Fotoğraf seç] |

### 6️⃣ SAVE Tıkla

---

## ✨ **Fotoğraf Ekleme**

Poster fotoğraflarını şu klasöre koy:
```
C:\Users\Helena\invoicer\media\posters\
```

Örnek dosyalar:
- `inception.jpg`
- `interstellar.png`
- vb.

---

## 🧪 **Test**

Admin panelinde 2-3 başlık ekledikten sonra:
```
http://localhost:5173/
```

Ana sayfada posterlerle birlikte filmler ve diziler göreceksin! 🎬

---

## ⚙️ **Teknik Detaylar**

| Ayar | Değer |
|------|-------|
| **MEDIA_URL** | `/media/` |
| **MEDIA_ROOT** | `C:\Users\Helena\invoicer\media` |
| **ALLOWED_HOSTS** | `['*']` |
| **DEBUG** | `True` |

✅ Tümü ayarlandı!

---

## ❌ **Hâlâ Çalışmıyorsa**

1. **Django sunucusunu kontrol et:**
   - Terminal'de `python manage.py runserver` çalışıyor mu?
   - `Starting development server at http://127.0.0.1:8000/` mesajı var mı?

2. **Tarayıcı Cache'i Temizle:**
   - Ctrl + Shift + Delete

3. **Backend Terminal Çıktısına Bak:**
   - Hata mesajı var mı?
   - 500 hatası var mı?

4. **Browser Console'u Aç (F12):**
   - Network tab'ında admin request'ini kontrol et

---

**Admin Panel artık hazır!** 🎉


