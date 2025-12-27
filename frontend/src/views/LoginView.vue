<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img alt="Logo" class="login-logo" src="@/assets/logo.svg" />
        <h1>Giriş Yap</h1>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">E-posta Adresi</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="example@example.com"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Şifre</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Şifrenizi girin"
            required
            class="form-input"
          />
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input v-model="form.rememberMe" type="checkbox" />
            <span>Beni hatırla</span>
          </label>
          <router-link to="/forgot-password" class="forgot-password">Şifrenizi mi unuttunuz?</router-link>
        </div>

        <button type="submit" class="login-button" :disabled="isLoading">
          <span v-if="!isLoading">Giriş Yap</span>
          <span v-else>Giriş yapılıyor...</span>
        </button>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
      </form>

      <div class="login-footer">
        <p>Hesabınız yok mu? <router-link to="/register" class="signup-link">Kaydol</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from 'axios'
const router = useRouter()
const form = ref({
  email: '',
  password: '',
  rememberMe: false
})

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''


try {

const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: form.value.email,
      password: form.value.password,
    })
    const token = response.data.token

    if (token) {

      localStorage.setItem('token', token)
      successMessage.value = 'Giriş başarılı! Yönlendiriliyorsunuz...'

      setTimeout(() => {
        router.push('/')
      }, 500)
    }
  } catch (error) {
    // Hata detayını terminale ve ekrana basalım
    console.error('Login Hatası Detayı:', error.response?.data)
    errorMessage.value = error.response?.data?.error || 'Giriş başarısız.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu',
    'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
}

.login-logo {
  width: 60px;
  height: 60px;
  margin-bottom: 15px;
  filter: brightness(0) invert(1);
}

.login-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.login-form {
  padding: 40px 30px;
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
  letter-spacing: 0.3px;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 13px;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #555;
  user-select: none;
}

.remember-me input {
  margin-right: 8px;
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: #667eea;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #764ba2;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  margin-bottom: 15px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  padding: 12px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c33;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: center;
}

.success-message {
  padding: 12px;
  background-color: #efe;
  border: 1px solid #cfc;
  border-radius: 6px;
  color: #3c3;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: center;
}

.login-footer {
  padding: 20px 30px;
  background-color: #f8f9fa;
  text-align: center;
  font-size: 14px;
  color: #666;
  border-top: 1px solid #e1e8ed;
}

.signup-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .login-container {
    padding: 15px;
  }

  .login-card {
    border-radius: 8px;
  }

  .login-header {
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .login-form {
    padding: 30px 20px;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .forgot-password {
    align-self: flex-end;
  }

  .login-footer {
    padding: 15px 20px;
  }
}
</style>

