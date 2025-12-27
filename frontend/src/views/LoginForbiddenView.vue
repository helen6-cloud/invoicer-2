<template>
  <div class="forbidden-container">
    <div class="forbidden-card">
      <div class="forbidden-header">
        <div class="error-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <h1>403 - Erişim Engellendi</h1>
        <p class="subtitle">Origin Kontrolü Başarısız</p>
      </div>

      <div class="forbidden-content">
        <div class="error-details">
          <h2>Ne Oldu?</h2>
          <p>
            Sisteme giriş yapmaya çalıştığınız sırada bir CORS (Cross-Origin Resource Sharing)
            hatası oluştu. Bu, genellikle güvenlik nedenlerinden dolayı web uygulamanızın
            API sunucusuyla iletişim kurmasının engellenmesini anlamına gelir.
          </p>

          <h3>Hata Detayları:</h3>
          <div class="error-box">
            <code>Origin checking failed - http://localhost:5173 does not match any trusted origins</code>
          </div>

          <h2>Olası Sebepler:</h2>
          <ul>
            <li>✗ Django backend'inde CORS ayarları yapılmamış</li>
            <li>✗ CORS middleware'i yanlış sırada veya eksik</li>
            <li>✗ Frontend URL'i backend'in güvenilen kaynaklar listesinde yok</li>
            <li>✗ API sunucusu çalışmıyor veya yanlış porttan erişiliyor</li>
          </ul>

          <h2>Çözüm Yolları:</h2>
          <div class="solutions">
            <div class="solution-step">
              <h4>1. Django Ayarlarını Kontrol Edin</h4>
              <p>Backend <code>settings.py</code> dosyasında şunları ekleyin:</p>
              <pre><code>INSTALLED_APPS = [
    'corsheaders',
    # ... diğer apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # ... diğer middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True</code></pre>
            </div>

            <div class="solution-step">
              <h4>2. Django Paketini Yükleyin</h4>
              <p>Eğer django-cors-headers yüklü değilse:</p>
              <pre><code>pip install django-cors-headers</code></pre>
            </div>

            <div class="solution-step">
              <h4>3. Sunucuyu Yeniden Başlatın</h4>
              <p>Django sunucusunu yeniden başlatın:</p>
              <pre><code>python manage.py runserver</code></pre>
            </div>

            <div class="solution-step">
              <h4>4. API URL'sini Kontrol Edin</h4>
              <p>Frontend'de doğru API endpoint'ini kullanın:</p>
              <pre><code>const response = await apiClient.post('auth/login/', {
  kullanici_adi: username,
  sifre: password
})</code></pre>
            </div>
          </div>

          <h2>Teknik Detaylar:</h2>
          <div class="tech-details">
            <p><strong>Frontend Adresi:</strong> http://localhost:5173</p>
            <p><strong>Backend Adresi:</strong> http://localhost:8000</p>
            <p><strong>API Endpoint:</strong> http://localhost:8000/api/auth/login/</p>
            <p><strong>Middleware Sırası Önemli:</strong> CorsMiddleware, SecurityMiddleware'den sonra gelmelidir</p>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="goHome" class="btn btn-primary">
            <span>Ana Sayfaya Dön</span>
          </button>
          <button @click="retryLogin" class="btn btn-secondary">
            <span>Tekrar Dene</span>
          </button>
          <button @click="openDocumentation" class="btn btn-tertiary">
            <span>Belgeleri Aç</span>
          </button>
        </div>
      </div>

      <div class="forbidden-footer">
        <p>Bu sorun devam ederse lütfen sistem yöneticisiyle iletişime geçin.</p>
        <p class="timestamp">Zaman: {{ new Date().toLocaleString('tr-TR') }}</p>
      </div>
    </div>

    <!-- Başka bir container - daha basit hata sayfası -->
    <div v-if="showSimpleVersion" class="simple-error-card">
      <h2>🔒 CORS Hatası</h2>
      <p>Backend'iniz CORS için yapılandırılmamış.</p>
      <p><strong>Çözüm:</strong> Django settings.py'ye CORS ayarlarını ekleyin.</p>
      <button @click="showSimpleVersion = false">Detaylı Bilgi Gör</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showSimpleVersion = ref(false)

const goHome = () => {
  router.push('/')
}

const retryLogin = () => {
  router.push('/login')
}

const openDocumentation = () => {
  // Belgeler sayfasını açabilir veya harici link açabilir
  window.open('https://django-cors-headers.readthedocs.io/', '_blank')
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.forbidden-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu',
    'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

.forbidden-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  max-width: 900px;
  width: 100%;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.forbidden-header {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  padding: 50px 40px;
  text-align: center;
  position: relative;
}

.error-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  opacity: 0.9;
  animation: pulse 2s ease-in-out infinite;
}

.error-icon svg {
  width: 100%;
  height: 100%;
  stroke: white;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.9;
  }
  50% {
    opacity: 0.7;
  }
}

.forbidden-header h1 {
  margin: 0 0 10px;
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.subtitle {
  margin: 0;
  font-size: 16px;
  opacity: 0.95;
  font-weight: 500;
}

.forbidden-content {
  padding: 40px;
}

.error-details {
  margin-bottom: 40px;
}

.error-details h2 {
  color: #1f2937;
  font-size: 20px;
  margin-top: 20px;
  margin-bottom: 12px;
  border-left: 4px solid #667eea;
  padding-left: 16px;
}

.error-details h2:first-child {
  margin-top: 0;
}

.error-details h3 {
  color: #374151;
  font-size: 16px;
  margin: 15px 0 10px;
}

.error-details h4 {
  color: #1f2937;
  font-size: 15px;
  margin: 0 0 8px;
}

.error-details p {
  color: #555;
  line-height: 1.6;
  margin: 0 0 15px;
}

.error-box {
  background: #f3f4f6;
  border-left: 4px solid #ef4444;
  padding: 15px;
  border-radius: 6px;
  margin: 15px 0;
  overflow-x: auto;
}

.error-box code {
  font-family: 'Courier New', monospace;
  color: #dc2626;
  font-size: 13px;
  word-break: break-word;
}

.error-details ul {
  list-style: none;
  padding: 0;
  margin: 15px 0;
}

.error-details li {
  padding: 8px 0;
  color: #555;
  font-size: 14px;
}

.solutions {
  margin: 20px 0;
}

.solution-step {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.solution-step:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}

.solution-step h4 {
  margin-top: 0;
  color: #667eea;
}

.solution-step pre {
  background: #1f2937;
  color: #f3f4f6;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 10px 0 0;
  font-size: 12px;
  line-height: 1.5;
}

.solution-step code {
  font-family: 'Courier New', monospace;
}

.tech-details {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  padding: 20px;
  border-radius: 6px;
  margin-top: 20px;
}

.tech-details p {
  margin: 8px 0;
  font-size: 14px;
  color: #1e40af;
}

.tech-details strong {
  color: #1e3a8a;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 30px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f3f4f6;
  color: #1f2937;
  border: 2px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.btn-tertiary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-tertiary:hover {
  background: #f8f9ff;
  border-color: #764ba2;
}

.forbidden-footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 20px 40px;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

.forbidden-footer p {
  margin: 5px 0;
}

.timestamp {
  font-size: 12px;
  opacity: 0.7;
}

.simple-error-card {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 300px;
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .forbidden-header {
    padding: 30px 20px;
  }

  .forbidden-header h1 {
    font-size: 28px;
  }

  .forbidden-content {
    padding: 25px;
  }

  .error-icon {
    width: 60px;
    height: 60px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .solution-step {
    padding: 15px;
  }

  .solution-step pre {
    font-size: 11px;
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .forbidden-card {
    border-radius: 8px;
  }

  .forbidden-header {
    padding: 20px;
  }

  .forbidden-header h1 {
    font-size: 24px;
  }

  .forbidden-content {
    padding: 15px;
  }

  .error-details h2 {
    font-size: 18px;
  }

  .error-details h3 {
    font-size: 14px;
  }

  .error-details p {
    font-size: 13px;
  }

  .error-box {
    padding: 10px;
  }

  .error-box code {
    font-size: 11px;
  }

  .solution-step {
    padding: 12px;
    margin-bottom: 12px;
  }

  .solution-step h4 {
    font-size: 14px;
  }

  .solution-step pre {
    font-size: 10px;
    padding: 10px;
  }
}
</style>

