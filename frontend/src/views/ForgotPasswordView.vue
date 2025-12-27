<template>
  <div class="forgot-container">
    <div class="forgot-card">
      <div class="forgot-header">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="lock-icon">
          <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 0 0-5.25 5.25v2.25H4.5A2.25 2.25 0 0 0 2.25 11.25v6.75a2.25 2.25 0 0 0 2.25 2.25h15a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25h-2.25V6.75A5.25 5.25 0 0 0 12 1.5Zm-1.5 6a3.75 3.75 0 1 1 7.5 0v2.25h-7.5V7.5Zm1.5 8.25a.75.75 0 0 0-1.5 0v3a.75.75 0 0 0 1.5 0v-3Z" clip-rule="evenodd" />
        </svg>
        <h1>Şifremi Sıfırla</h1>
      </div>

      <form @submit.prevent="handleResetRequest" class="forgot-form">
        <p class="form-description">
          Hesabınıza kayıtlı e-posta adresinizi girin. Şifre sıfırlama bağlantısını size göndereceğiz.
        </p>

        <div class="form-group">
          <label for="email">E-posta Adresi</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Kayıtlı e-posta adresiniz"
            required
            class="form-input"
          />
        </div>

        <button type="submit" class="reset-button" :disabled="isLoading">
          <span v-if="!isLoading">Bağlantı Gönder</span>
          <span v-else>Gönderiliyor...</span>
        </button>

        <Transition name="fade">
          <div v-if="errorMessage" class="message error-message">
            {{ errorMessage }}
          </div>
          <div v-else-if="successMessage" class="message success-message">
            {{ successMessage }}
          </div>
        </Transition>

      </form>

      <div class="forgot-footer">
        <router-link to="/login" class="back-to-login">
          <small>Giriş Ekranına Geri Dön</small>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import apiClient from '@/api/axios'

const router = useRouter()
const email = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleResetRequest = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true



  try {
    const response = await apiClient.post('/auth/users/reset_password/', {
      email: email.value,
    })


    if (response.status === 204 || response.status === 200) {
      successMessage.value = 'Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.'

      setTimeout(() => {
         router.push('/login')
      }, 5000)
    } else {
      throw new Error('İstek gönderilirken beklenmeyen bir hata oluştu.')
    }

  } catch (error) {

    const msg = error.response?.data?.email?.[0]
                || error.response?.data?.detail
                || 'E-posta adresi bulunamadı veya bir hata oluştu.'
    errorMessage.value = msg
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Genel Yapı ve Animasyon Temelleri */
.forgot-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1d2b64 0%, #f8cdda 100%);
  padding: 20px;
}

.forgot-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 450px;
  overflow: hidden;
  /* Başlangıç animasyonu */
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.forgot-header {
  background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
  color: white;
  padding: 30px 20px;
  text-align: center;
}

.lock-icon {
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.2));
  /*Sallanma animasyonu*/
  animation: shake 0.9ms ease-in-out infinite alternate;
}

@keyframes shake {
  from { transform: rotate(-3deg); }
  to { transform: rotate(3deg); }
}

.forgot-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.forgot-form {
  padding: 30px;
}

.form-description {
  margin-bottom: 25px;
  font-size: 14px;
  color: #555;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

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
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4ca1af;
  box-shadow: 0 0 0 3px rgba(76, 161, 175, 0.3);
}

.reset-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(90deg, #4ca1af 0%, #2c3e50 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(44, 62, 80, 0.2);
}

.reset-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 161, 175, 0.4);
}

.reset-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transition: opacity 0.5s;
}

/* Mesajlar */
.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;

  overflow: hidden;
}

.error-message {
  background-color: #ffe0e0;
  border: 1px solid #ff5555;
  color: #cc0000;
}

.success-message {
  background-color: #e0fff2;
  border: 1px solid #00c49f;
  color: #008060;
}


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.forgot-footer {
  padding: 15px 30px;
  background-color: #f7f7f7;
  text-align: center;
  border-top: 1px solid #eee;
}

.back-to-login {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.back-to-login:hover {
  color: #4ca1af;
}
</style>