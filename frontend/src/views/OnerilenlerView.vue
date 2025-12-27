<template>
  <div class="main-container">
    <div class="content-wrapper">
      <h1 class="page-title animate-fade">✨ Sizin İçin Önerilenler</h1>

      <div class="tabs-container animate-fade">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Yapay zeka önerileri hazırlıyor...</p>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>

      <div v-else-if="filteredItems.length > 0" class="titles-grid">
        <div
          v-for="(item, index) in filteredItems"
          :key="item.id"
          class="movie-card animate-up"
          :style="{ '--delay': index }"
        >
          <div class="card-image">
            <img
              :src="item.poster || 'https://via.placeholder.com/280x400?text=No+Poster'"
              class="poster-img"
              alt="poster"
              @error="(e) => e.target.src = 'https://via.placeholder.com/280x400?text=No+Poster'"
            />

            <div class="card-badges">
              <span class="badge-type">{{ item.cesit === 'movie' ? 'Film' : 'Dizi' }}</span>
              <span class="badge-score" v-if="item.imdb_puan">⭐ {{ item.imdb_puan }}</span>
            </div>

            <div class="card-top-actions">
              <div class="action-btn" @click.stop="toggleFavorite(item)" :class="{ 'active': favoritedTitles.has(item.id) }" title="Favorilere Ekle">
                {{ favoritedTitles.has(item.id) ? '❤️' : '🤍' }}
              </div>

              <div class="action-btn" @click.stop="toggleWatchlist(item)" :class="{ 'active': watchlistTitles.has(item.id) }" title="Listeme Ekle">
                {{ watchlistTitles.has(item.id) ? '✅' : '➕' }}
              </div>

              <div class="action-btn" @click.stop="toggleWatched(item)" :class="{ 'active': watchedTitles.has(item.id) }" title="Daha Önce İzledim">
                {{ watchedTitles.has(item.id) ? '👁️' : '⚪' }}
              </div>
            </div>

            <div class="card-overlay" @click.stop="viewDetails(item)">
              <button class="view-btn">Detayları Gör</button>
            </div>
          </div>

          <div class="card-details">
            <div class="title-row">
              <h3>{{ item.title_name }}</h3>
            </div>
            <div class="card-meta">
              <span class="m-year">{{ item.yil }}</span>
              <span class="m-dot">•</span>
              <span class="m-duration" v-if="item.sure">{{ item.sure }} dk</span>
              <span class="m-dot">•</span>
              <span class="m-genre">{{ item.turler ? item.turler.slice(0, 2).join(', ') : 'Genel' }}</span>
            </div>
            <p class="mini-ozet">{{ item.ozet ? item.ozet.substring(0, 60) + '...' : 'Özet bulunamadı.' }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <p>😔 Bu kategoride henüz öneri bulunamadı.</p>
      </div>
    </div>

    <TitleDetailModal
      v-if="showModal"
      :isOpen="showModal"
      :title="selectedTitle || {}"
      :favoritedTitles="favoritedTitles"
      @close="closeModal"
    />
  </div>
</template>

<script>
import apiClient from '@/api/axios'
import TitleDetailModal from '@/components/TitleDetailModal.vue'

export default {
  name: "OnerilenlerView",
  components: { TitleDetailModal },
  data() {
    return {
      items: [],
      loading: false,
      error: null,
      activeTab: 'all', // 'all', 'movie', 'series'
      tabs: [
        { id: 'all', label: 'Tümü' },
        { id: 'movie', label: 'Filmler' },
        { id: 'series', label: 'Diziler' }
      ],
      // Kullanıcı etkileşimleri için Set yapıları
      favoritedTitles: new Set(),
      watchlistTitles: new Set(),
      watchedTitles: new Set(),

      showModal: false,
      selectedTitle: null
    };
  },
  computed: {
    // 4. Tab Filtreleme Mantığı
    filteredItems() {
      if (this.activeTab === 'all') return this.items;

      return this.items.filter(item => {
        const type = (item.cesit || '').toLowerCase();
        if (this.activeTab === 'movie') return type.includes('movie') || type.includes('film');
        if (this.activeTab === 'series') return type.includes('series') || type.includes('dizi');
        return true;
      });
    }
  },
  async mounted() {
    const token = localStorage.getItem("authToken") || localStorage.getItem("token");
    if (!token) {
      this.$router.push('/login');
      return;
    }

    await this.fetchRecommended();
    await this.fetchUserInteractions(); // Mevcut favori/listeleri çek
  },
  methods: {
    async fetchRecommended() {
      try {
        this.loading = true;
        this.error = null;
        const response = await apiClient.get('onerilenler/');
        this.items = response.data;
      } catch (err) {
        console.error("Fetch error:", err);
        this.error = "Öneriler alınırken bir hata oluştu.";
      } finally {
        this.loading = false;
      }
    },

    // Kullanıcının daha önce eklediklerini kontrol et (Kalplerin dolu gelmesi için)
    async fetchUserInteractions() {
      try {
        const [favRes, listRes] = await Promise.all([
          apiClient.get('favoriler/'),
          apiClient.get('izlenecekler/')
        ]);

        this.favoritedTitles = new Set(favRes.data.map(f => f.title));
        // İzlenecekler listesi yapısı farklı olabilir, 'title.id' veya direkt 'title' kontrol edilmeli
        this.watchlistTitles = new Set(listRes.data.map(l => l.title.id || l.title));
      } catch (err) {
        console.error("Etkileşim verileri çekilemedi", err);
      }
    },

    // --- FAVORİ İŞLEMLERİ ---
    async toggleFavorite(item) {
      try {
        // Zaten favorideyse çıkar (Backend'de ID bulmak lazım, burada basit toggle simülasyonu)
        // Gerçek silme işlemi için favori ID'si gerekir.
        // Basitlik adına burada sadece Ekleme/Silme logic'i:

        if (this.favoritedTitles.has(item.id)) {
           // Silme işlemi için favori objesinin ID'sini bulmak gerekir,
           // Şimdilik UI'da kaldırıyoruz, Backend entegrasyonu için fetchUserInteractions'daki ID'yi saklamak gerekebilir.
           // Hızlı çözüm: Tekrar fetch atarak ID bulup silmek:
           const res = await apiClient.get('favoriler/');
           const favObj = res.data.find(f => f.title === item.id);
           if(favObj) await apiClient.delete(`favoriler/${favObj.id}/`);

           this.favoritedTitles.delete(item.id);
        } else {
          await apiClient.post('favoriler/', { title: item.id });
          this.favoritedTitles.add(item.id);
        }
        this.favoritedTitles = new Set(this.favoritedTitles); // Reaktiflik için
      } catch (err) {
        alert("İşlem başarısız: " + err.message);
      }
    },

    // --- İZLENECEKLER LİSTESİ ---
    async toggleWatchlist(item) {
      try {
        if (this.watchlistTitles.has(item.id)) {
           // Silme mantığı (Favori ile aynı mantıkta backend ID gerekir)
           const res = await apiClient.get('izlenecekler/');
           const listObj = res.data.find(l => (l.title.id || l.title) === item.id);
           if(listObj) await apiClient.delete(`izlenecekler/${listObj.id}/`);

           this.watchlistTitles.delete(item.id);
        } else {
          await apiClient.post('izlenecekler/', { title: item.id });
          this.watchlistTitles.add(item.id);
        }
        this.watchlistTitles = new Set(this.watchlistTitles);
      } catch (err) {
        console.error(err);
      }
    },

    // --- İZLEDİM BUTONU (Opsiyonel Backend Endpoint'i Varsa) ---
    async toggleWatched(item) {
      // Backend'de "izlenenler" endpoint'i yoksa sadece local görsel değişim yapabiliriz
      // Veya custom bir endpoint kullanabilirsin.
      if (this.watchedTitles.has(item.id)) {
        this.watchedTitles.delete(item.id);
      } else {
        this.watchedTitles.add(item.id);
        // await apiClient.post('izlenenler/', { title: item.id }); // Backend varsa aç
      }
      this.watchedTitles = new Set(this.watchedTitles);
    },

    viewDetails(item) {
      this.selectedTitle = item;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedTitle = null;
    }
  }
};
</script>

<style scoped>
/* GENEL SAYFA STİLİ (Diğer sayfalarla uyumlu) */
.main-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1c2c 0%, #0d0e1b 100%);
  color: white;
  padding: 40px 20px;
  font-family: 'Poppins', sans-serif;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  font-size: 36px;
  margin-bottom: 30px;
  background: linear-gradient(to right, #ffcc00, #ff6b6b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

/* TABLAR (FİLM/DİZİ AYRIMI) */
.tabs-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 40px;
}

.tab-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  padding: 10px 25px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  font-weight: 600;
}

.tab-btn:hover, .tab-btn.active {
  background: #ffcc00;
  color: #1a1c2c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 204, 0, 0.3);
}

/* KART GRID YAPISI */
.titles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 30px;
}

.movie-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  animation: fadeUp 0.6s ease forwards;
  opacity: 0;
  animation-delay: calc(var * 0.1s);
}

.movie-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
}

.card-image {
  height: 340px;
  position: relative;
  overflow: hidden;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.movie-card:hover .poster-img {
  transform: scale(1.05);
}

/* BUTON GRUBU (SAĞ ÜST) */
.card-top-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 5;
}

.action-btn {
  width: 38px;
  height: 38px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s;
  font-size: 16px;
  color: white;
}

.action-btn:hover {
  background: white;
  color: black;
  transform: scale(1.1);
}

.action-btn.active {
  background: white;
  color: red; /* Kalp için varsayılan */
}

/* ROZETLER */
.card-badges {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.badge-type, .badge-score {
  background: rgba(255, 204, 0, 0.9);
  color: #1a1c2c;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
}
.badge-score { background: rgba(0,0,0,0.7); color: #ffcc00; }

/* OVERLAY VE DETAY BUTONU */
.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: 0.3s;
  cursor: pointer;
}

.movie-card:hover .card-overlay { opacity: 1; }

.view-btn {
  background: #ffcc00;
  color: #1a1c2c;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  transform: translateY(20px);
  transition: 0.3s;
}

.movie-card:hover .view-btn { transform: translateY(0); }

/* KART ALT DETAYLARI */
.card-details {
  padding: 15px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}

.title-row h3 {
  font-size: 16px;
  margin: 0 0 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-meta {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 8px;
}

.mini-ozet {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.4;
  margin: 0;
}

.m-dot { margin: 0 5px; }

/* YÜKLENİYOR VE HATA */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.5);
}

.spinner {
  width: 40px; height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: #ffcc00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

.error-msg {
  color: #ff6b6b;
  text-align: center;
  padding: 20px;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 10px;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>