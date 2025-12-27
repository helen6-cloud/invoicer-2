<template>
  <div class="profile-page">
    <div class="card">
      <div class="avatar-wrap">
        <img :src="profile.avatar || placeholder" alt="Profil resmi" class="avatar" />
      </div>

      <h2 class="name">{{ profile.kullanici_adi || 'Kullanıcı' }}</h2>
      <p class="email" v-if="profile.email">{{ profile.email }}</p>
      <p class="meta">Kayıt: <span>{{ formattedDate(profile.kayit_tarihi) }}</span></p>

      <div class="actions">
        <button class="btn edit" @click="goEdit">Profili Düzenle</button>
        <button class="btn password" @click="goChangePassword">Şifre Değiştir</button>
        <button class="btn logout" @click="handleLogout">Çıkış Yap</button>
      </div>

      <div v-if="loading" class="info">Yükleniyor...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios' // projenizde axios için kullanılan dosya; yoksa './api/axios' kullanın

const router = useRouter()
const placeholder = 'https://via.placeholder.com/150?text=Profil'

// Durumlar
const loading = ref(false)
const error = ref('')
const success = ref('')
const profile = ref({})

// Yardımcı: tarih formatı
function formattedDate(dateStr) {
  if (!dateStr) return '-'
  try {
    const d = new Date(dateStr)
    return d.toLocaleString()
  } catch {
    return dateStr
  }
}

// Eğer kullanıcı girişli değilse yönlendir
function requireAuthOrRedirect() {
  const token = localStorage.getItem('token') || localStorage.getItem('userToken')
  if (!token) {
    router.push('/login')
    return false
  }
  return token
}

// Profil verisini backend'den çek
async function fetchProfile() {
  const token = requireAuthOrRedirect()
  if (!token) return

  loading.value = true
  error.value = ''
  try {
    const res = await axios.get('/profiles/', {
      headers: { Authorization: `Token ${token}` }
    })
    // Beklenen: backend kullanıcının profillerini döndürüyor olabilir.
    // Eğer liste dönerse ilkini al (uyarlama gerekirse backend ile eşleştir).
    if (Array.isArray(res.data)) {
      profile.value = res.data[0] || {}
    } else {
      profile.value = res.data || {}
    }
  } catch (err) {
    console.error('Profil çekme hatası', err)
    error.value = 'Profil bilgileri alınamadı.'
  } finally {
    loading.value = false
  }
}

// Buton metodları
function goEdit() {
  router.push('/profil/duzenle') // router'da bu yol varsa açar; yoksa sonraki adımda ekleyelim
}
function goChangePassword() {
  router.push('/forgot-password') // veya '/change-password' backend endpointine göre değiştir
}
function handleLogout() {
  localStorage.removeItem('token')
  localStorage.removeItem('userToken')
  success.value = 'Çıkış yapıldı.'
  setTimeout(() => router.push('/login'), 700)
}

// Component lifecycle
onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px;
  background: linear-gradient(180deg,#0f172a 0%, #071132 100%);
  color: #fff;
}

.card {
  width: 100%;
  max-width: 720px;
  background: rgba(255,255,255,0.04);
  border-radius: 14px;
  padding: 28px;
  box-shadow: 0 8px 30px rgba(2,6,23,0.6);
  text-align: center;
  animation: cardIn 450ms cubic-bezier(.2,.9,.3,1);
}

@keyframes cardIn {
  from { transform: translateY(12px); opacity: 0 }
  to   { transform: translateY(0); opacity: 1 }
}

.avatar-wrap {
  display:flex;
  justify-content:center;
  margin-bottom: 12px;
}

.avatar {
  width: 110px;
  height: 110px;
  border-radius: 999px;
  object-fit: cover;
  border: 4px solid rgba(124,58,237,0.9);
  box-shadow: 0 8px 24px rgba(2,6,23,0.6);
}

.name {
  margin: 6px 0 4px;
  font-size: 22px;
  font-weight: 700;
}

.email {
  color: rgba(255,255,255,0.8);
  margin-bottom: 8px;
}

.meta {
  color: rgba(255,255,255,0.6);
  font-size: 13px;
  margin-bottom: 18px;
}

.actions {
  display:flex;
  gap: 12px;
  justify-content:center;
  flex-wrap:wrap;
  margin-top: 6px;
}

.btn {
  padding: 10px 14px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  min-width: 150px;
  transition: transform .18s ease, box-shadow .18s ease;
}

.btn:hover { transform: translateY(-4px) }

.edit {
  background: linear-gradient(90deg,#6d28d9,#8b5cf6);
  color: white;
  box-shadow: 0 10px 30px rgba(139,92,246,0.14);
}

.password {
  background: linear-gradient(90deg,#06b6d4,#0ea5a4);
  color: white;
  box-shadow: 0 10px 30px rgba(6,182,212,0.12);
}

.logout {
  background: linear-gradient(90deg,#ef4444,#fb7185);
  color: white;
  box-shadow: 0 10px 30px rgba(239,68,68,0.12);
}

.info { margin-top:12px; color: #cbd5e1 }
.error { margin-top:12px; color: #ff7b7b }
.success { margin-top:12px; color: #7ef0a6 }
</style>

