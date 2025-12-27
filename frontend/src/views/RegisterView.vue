<template>
  <div class="register-container" :class="themeClass">
<transition name="fade-scale">
  <div v-if="showSuccessAnimation" class="success-overlay">
    <Vue3Lottie
      :animationData="successAnimation"
      :loop="false"
      :speed="1"
      style="width: 320px; height: 320px"
    />
    <p class="success-text">Kayıt Başarılı 🎉</p>
  </div>
</transition>

<div class="edge-figures"  :class="{ celebrate: isSuccess }">
  <span
    v-for="n in 6"
    :key="n"
    class="runner"
    :class="{ clap: isSuccess }"
    :style="getRunnerStyle(n)"
  >
    {{ getRunnerIcon(n) }}
  </span>
</div>

    <div class="register-card">
      <div class="register-header">
        <h1>Hesap Oluştur</h1>
      </div>
    <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">Kullanıcı Adı</label>
          <input v-model="form.username" type="text" id="username" required class="form-input" placeholder="Kullanıcı adınız" />
        </div>

        <div class="form-group">
          <label for="email">E-posta Adresi</label>
          <input v-model="form.email" type="email" id="email" required class="form-input" placeholder="example@mail.com" />
        </div>

        <div class="form-group">
          <label for="password">Şifre</label>
          <input v-model="form.password" type="password" id="password" required class="form-input" placeholder="Şifrenizi girin" />
        </div>

        <div class="form-group">
          <label for="password2">Şifre Tekrar</label>
          <input v-model="form.password2" type="password" id="password2" required class="form-input" placeholder="Şifrenizi tekrar girin" />
          <p v-if="form.password !== form.password2 && form.password2" class="error-inline">Şifreler eşleşmiyor!</p>
        </div>

        <div class="form-group gender-select">
          <label>Cinsiyet</label>
          <div class="gender-options">
            <label class="gender-radio">
              <input type="radio" v-model="form.gender" value="female" name="gender" />
              <span class="radio-label">Kadın</span>
            </label>
            <label class="gender-radio">
              <input type="radio" v-model="form.gender" value="male" name="gender" />
              <span class="radio-label">Erkek</span>
            </label>
          </div>
        </div>

        <button type="submit" class="register-button" :disabled="isLoading || form.password !== form.password2">
          <span v-if="!isLoading">Hemen Kaydol</span>
          <span v-else>Kaydolunuyor...</span>
        </button>

        <Transition name="fade">
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          <div v-else-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
        </Transition>

      </form>

      <div class="register-footer">
        <p>Zaten hesabınız var mı? <router-link to="/login" class="login-link">Giriş Yap</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Vue3Lottie } from 'vue3-lottie'
import successAnimation from '@/assets/animations/RabbitHi.json'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/axios'
const showSuccessAnimation = ref(false)
const isSuccess = ref(false)
const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
  gender: '',
})

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Cinsiyete göre arka plan teması sınıfını hesaplar
const themeClass = computed(() => {
  return form.value.gender === 'male' ? 'male-theme' : 'female-theme'
})

const RUNNER_ICONS_FEMALE = ['🏃‍♀️', '🧚‍♀️', '🐇', '🦋']
const RUNNER_ICONS_MALE = ['🏃‍♂️', '🦸‍♂️', '🐕', '🐎']

const getRunnerIcon = (n) => {
  const icons = form.value.gender === 'male'
    ? RUNNER_ICONS_MALE
    : RUNNER_ICONS_FEMALE
  return icons[n % icons.length]
}

const getRunnerStyle = (n) => {
  const side = n % 2 === 0 ? 'left' : 'right'
  const top = (n * 12) % 90
  const duration = 10 + (n % 6)
  const delay = -(n * 2)

  return {
    top: `${top}%`,
    [side]: '-40px',
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`
  }
}
const handleRegister = async () => {
  if (form.value.password !== form.value.password2) {
    errorMessage.value = 'Şifreler eşleşmiyor!'
    return
  }

  const dataToSend = {
    username: form.value.username,
    email: form.value.email,
    password: form.value.password,
    password2: form.value.password2,
    gender: form.value.gender === 'male' ? 'M' : form.value.gender === 'female' ? 'F' : 'O',
  }

  try {
    isLoading.value = true

    const response = await apiClient.post('auth/register/', dataToSend)

    if (response.status === 201 || response.data?.token) {
      errorMessage.value = ''
      successMessage.value = 'Kayıt başarılı. Yönlendiriliyorsunuz...'

      if (response.data?.token) {
        localStorage.setItem('authToken', response.data.token)
      }

      showSuccessAnimation.value = true
isSuccess.value = true
errorMessage.value = ''
successMessage.value = ''

setTimeout(() => {
  router.push('/')
}, 1800)
    }

  } catch (error) {
    console.error('Register Error:', error)

    if (error.response?.status === 400) {
      const errors = error.response.data
      errorMessage.value = Object.values(errors)[0] || 'Kayıt başarısız'
      return
    }

    errorMessage.value = 'Sunucu hatası'
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
/* --------- KART YAPISI VE ARKA PLAN İÇİN GÜNCELLENMİŞ STİLLER --------- */

/* Global Temizlik */
:global(html), :global(body) {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* GENEL KONTEYNER (Dinamik Arka Plan) */
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: background 0.8s ease-in-out;
}

.register-card {
  /* LoginView'den alınan şık kart stili */
  background: white;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  width: 100%;
  max-width: 420px; /* LoginView'deki max genişlik */
  z-index: 10;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.register-header {
  /* LOGIN STİLİNE GÖRE GRADYAN BAŞLIK */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
  margin-bottom: 0; /* İçerik ile birleşik durmaması için */
}

.register-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.register-form {
  padding: 30px 40px;
}

/* --------- TEMA TANIMLARI (Dinamik Arka Planın Kontrolü) --------- */

/* KADIN TEMASI (Pastel Pembe/Mor) */
.female-theme {
  --theme-color: #764ba1
; /* Ana Tema Rengi (Butonlar İçin) */
  --theme-rgb: 118, 75, 162;
  --bg-light: #dc7bdc;
  --bg-dark: #e0b4ff;
  background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-dark) 100%);
}

/* ERKEK TEMASI (Mavi/Yeşil Tonları) */
.male-theme {
  --theme-color: #00bcd4;
  --theme-rgb: 0, 188, 212;
  --bg-light: #5cadbf;
  --bg-dark: #65d0bd;
  background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-dark) 100%);
}


/* --------- FORM VE BUTON STİLLERİ (Login Stilinden Alındı) --------- */

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  /* Odak rengi Login'deki gibi mor/lila */
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.error-inline {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.register-button {
  width: 100%;
  padding: 12px;
  /* Login'deki mor gradyan buton stili */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color:black;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  margin-top: 15px;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  padding: 20px 40px;
  background-color: #f8f9fa;
  text-align: center;
  font-size: 14px;
  color: #666;
  border-top: 1px solid #e1e8ed;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.gender-radio input:checked + .radio-label {
  background-color: var(--theme-color);
  border-color: var(--theme-color);
  color: white;
  box-shadow: 0 4px 10px rgba(var(--theme-rgb), 0.3);
}

.object-icon {
    font-size: 30px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 1;
    user-select: none;
}




.edge-figures {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

.runner {
  position: absolute;
  font-size: 28px;
  animation-name: runAcross;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  opacity: 0.9;
}


@keyframes runAcross {
  0% {
    transform: translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(-110vw);
    opacity: 0;
  }
}


.runner[right] {
  animation-name: runAcrossReverse;
}

@keyframes runAcrossReverse {
  0% {
    transform: translateX(0);
    opacity: 0;
  }
  100% {
    transform: translateX(110vw);
    opacity: 0;
  }

}
/* Başarı durumunda koşma dursun */
.celebrate .runner {
  animation: clap 0.8s ease-in-out infinite;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%);
  font-size: 40px;
}

/* Alkış efekti */
@keyframes clap {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.2); }
  100% { transform: translate(-50%, -50%) scale(1); }
}
.success-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(6px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.success-text {
  color: white;
  font-size: 22px;
  margin-top: 10px;
  font-weight: 600;
}

/* Animasyon geçişi */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.4s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

</style>