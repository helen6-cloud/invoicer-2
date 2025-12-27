<template>
  <div class="main-container">
    <aside class="sidebar">
  <div class="logo-area">
    <span class="logo-icon">🎬</span>
    <h2 class="logo-text">Filmler</h2>
  </div>

  <div class="filter-group">
    <p class="filter-label">Kategoriler</p>
    <div class="modern-tabs">
      <button
        v-for="group in groups"
        :key="group.id"
        :class="['modern-tab-btn', { active: selectedGroup === group.id }]"
        @click="changeGroup(group.id)"
      >
        <span class="dot"></span>
        {{ group.label }}
      </button>
    </div>
  </div>

  <div class="filter-group mt-4">
    <p class="filter-label">Türler</p>
    <div class="genre-cloud">
      <div
      class="genre-chip"
      :class="{ active: selectedGenres.length === 0 }"
      @click="selectedGenres = []; fetchMovies()"
      >
        Hepsi
      </div>
      <div
        v-for="genre in allGenres"
        :key="genre.id"
        class="genre-chip"
        :class="{ active: selectedGenres.includes(genre.baslik) }"
        @click="toggleGenre(genre.baslik)"
      >
        {{ genre.baslik }}
        <span v-if="selectedGenres.includes(genre.baslik)" class="remove-icon">×</span>
      </div>
    </div>
  </div>
</aside>

    <main class="content-area">
      <header class="top-nav">
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Film, dizi veya oyuncu ara..."
            @input="filterMovies"
          />
        </div>
        <div class="user-stats">
          <span>{{ filteredMovies.length }} Sonuç</span>
        </div>
      </header>

      <section class="movies-explorer">
        <div v-if="loadingMovies" class="loader-container">
          <div class="spinner"></div>
          <p>Kütüphane taranıyor...</p>
        </div>

        <div v-else-if="movieError" class="error-msg">{{ movieError }}</div>

        <div class="titles-grid">
          <div
            v-for="(movie, index) in filteredMovies"
            :key="movie.id"
            class="movie-card"
            :style="{ '--delay': index }"
          >
            <div class="card-image">

<img
  :src="movie.poster_url || noPosterImg"
  @error="handleImageError"
  class="poster-img"
  alt="film posteri"
>
             <div class="card-badges">
  <span class="badge-type">
    {{ (movie.cesit || '').toLowerCase().includes('movie') || (movie.cesit || '').toLowerCase().includes('film') ? 'Film' : 'Dizi' }}
  </span>
</div>

              <div class="card-top-actions">
                <div class="action-btn fav-btn" @click.stop="toggleFavorite(movie)" :class="{ 'active': favoritedTitles.has(movie.id) }">
                  {{ favoritedTitles.has(movie.id) ? '❤️' : '🤍' }}
                </div>
                <div class="action-btn watchlist-btn" @click.stop="toggleWatchlist(movie)" :class="{ 'active': watchlistTitles.has(movie.id) }">
                  {{ watchlistTitles.has(movie.id) ? '✅' : '➕' }}
                </div>
              </div>

              <div class="card-overlay" @click.stop="viewDetails(movie)">
                <button class="view-btn">Detayları Gör</button>
              </div>
            </div>

            <div class="card-details">
              <div class="title-row">
                <h3>{{ movie.title_name }}</h3>
                <span
                  class="watched-status"
                  @click.stop="toggleWatched(movie)"
                  :class="{ 'is-watched': watchedTitles.has(movie.id) }"
                >
                  ✔
                </span>
              </div>
              <div class="card-meta">
                <span class="m-year">{{ movie.yil }}</span>
                <span class="m-dot">•</span>
                <span class="m-duration">{{ movie.sure }} dk</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!loadingMovies && filteredMovies.length === 0" class="empty-state">
          <p>Aradığınız kriterlere uygun içerik bulunamadı.</p>
        </div>
      </section>
    </main>

    <TitleDetailModal
     v-if="showModal"
     :isOpen="showModal"
     :title="selectedTitle"
     @close="closeModal"
     @status-changed="handleStatusChange"
    />
  </div>
</template>
<script>
import noPoster from '@/assets/no-poster.jpg'
import apiClient from '@/api/axios'
import TitleDetailModal from '@/components/TitleDetailModal.vue'

export default {
  name: 'MoviesView',
  components: { TitleDetailModal },
  data() {
    return {
      noPosterImg: noPoster,
      allMovies: [],
      filteredMovies: [],
      allGenres: [],
      loadingMovies: false,
      movieError: null,
      searchQuery: '',
      selectedGroup: 'genel',
      selectedGenres: [],
      selectedTitle: null,
      showModal: false,
      favoritedTitles: new Set(),
      watchlistTitles: new Set(),
      watchedTitles: new Set(),
      groups: [
        { id: 'genel', label: 'Genel' },
        { id: 'turk', label: 'Türk Yapımları' },
        { id: 'anime', label: 'Animeler' },
        { id: 'kore', label: 'Kore Dizileri' }
      ]
    }
  },
async mounted() {
  this.checkAuth();
  await Promise.all([
    this.fetchGenres(),
    this.fetchMovies(),
    this.fetchFavorites(),
    this.fetchWatchedStatus()
  ]);
},
  methods: {
    async fetchWatchedStatus() {
  try {
    const response = await apiClient.get('izlenenler/', { headers: this.getAuthHeader() });
    this.watchedTitles = new Set(response.data.map(w => w.title));
    this.filterMovies();
  } catch (err) {
    console.error("İzlenenler listesi çekilemedi:", err);
  }
},

  changeGroup(groupId) {
  console.log("Seçilen Grup:", groupId);
  this.selectedGroup = groupId;
  this.selectedGenres = [];
  this.fetchMovies();
},
    getAuthHeader() {
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');
      return token ? { Authorization: `Token ${token}` } : {};
    },

    checkAuth() {
      if (!localStorage.getItem('token') && !localStorage.getItem('authToken')) {
        this.$router.push('/login');
      }
    },

  toggleGenre(genreTitle) {

    const index = this.selectedGenres.indexOf(genreTitle);
    if (index > -1) {
      this.selectedGenres.splice(index, 1);
    } else {
      this.selectedGenres.push(genreTitle);
    }
    this.fetchMovies();
  },
    async fetchGenres() {
      try {
        const response = await apiClient.get('turler/', { headers: this.getAuthHeader() });
        this.allGenres = response.data;
      } catch (err) { console.error("Türler hatası:", err); }
    },

async fetchMovies() {
    this.loadingMovies = true;
    try {
      const response = await apiClient.get('titles/', {
        params: {
          grup: this.selectedGroup,

          kategori: this.selectedGenres.length > 0 ? this.selectedGenres.join(',') : undefined
        },
        headers: this.getAuthHeader()
      });


      this.allMovies = response.data.filter(item => {
        const type = (item.cesit || '').toLowerCase();

        return type.includes('film') || type.includes('movie');
      });

      this.filteredMovies = [...this.allMovies];
      this.filterMovies();
    } catch (err) {
      console.error("API Hatası:", err);
      this.movieError = "Filmler yüklenemedi.";
    } finally {
      this.loadingMovies = false;
    }
},
    async fetchFavorites() {
      try {
        const response = await apiClient.get('favoriler/', { headers: this.getAuthHeader() });
        this.favoritedTitles = new Set(response.data.map(f => f.title));
      } catch (err) { console.error("Favori çekme hatası:", err); }
    },

    async toggleFavorite(movie) {
      try {

        const response = await apiClient.get('favoriler/', { headers: this.getAuthHeader() });
        const fav = response.data.find(f => f.title === movie.id);

        if (fav) {
          await apiClient.delete(`favoriler/${fav.id}/`, { headers: this.getAuthHeader() });
          this.favoritedTitles.delete(movie.id);
        } else {
          await apiClient.post('favoriler/', { title: movie.id }, { headers: this.getAuthHeader() });
          this.favoritedTitles.add(movie.id);
        }

        this.favoritedTitles = new Set(this.favoritedTitles);
      } catch (err) {
        console.error('Favori işlemi başarısız. Token geçersiz veya endpoint hatalı.', err);
      }
    },

    viewDetails(movie) {
      this.selectedTitle = movie;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedTitle = null;
    },

   filterMovies() {
    let baseList = this.allMovies.filter(m => !this.watchedTitles.has(m.id));
  if (!this.searchQuery.trim()) {
    this.filteredMovies = baseList;
    return;
  }
  const query = this.searchQuery.toLowerCase();
  this.filteredMovies = baseList.filter(m =>
    m.title_name.toLowerCase().includes(query)
  );
},

    handleImageError(event) {

  if (event.target.src === this.noPosterImg) return;


  event.target.src = this.noPosterImg;
},
    handleStatusChange(id, status) {
  if (status === 'watched') {
    this.watchedTitles.add(id);
    this.watchedTitles = new Set(this.watchedTitles);
  }
},

    toggleWatchlist(movie) {
      if (this.watchlistTitles.has(movie.id)) this.watchlistTitles.delete(movie.id);
      else this.watchlistTitles.add(movie.id);
      this.watchlistTitles = new Set(this.watchlistTitles);
    },

    async toggleWatched(movie) {
  try {
    // İzleme geçmişini yöneten endpoint'iniz (Örn: /izlenenler/)
    // Bu kısım backend yapınıza göre değişebilir.
    if (this.watchedTitles.has(movie.id)) {
      // Eğer izlendiyse, kaydı silmek için DELETE atılabilir
      // await apiClient.delete(`izlenenler/${movie.id}/`, { headers: this.getAuthHeader() });
      this.watchedTitles.delete(movie.id);
    } else {
      // İşaretlendiğinde POST atılır
      await apiClient.post('izlenenler/', { title: movie.id, status: 'watched' }, { headers: this.getAuthHeader() });
      this.watchedTitles.add(movie.id);
    }

    this.watchedTitles = new Set(this.watchedTitles);
    this.filterMovies();

  } catch (err) {
    console.error('İzlenme durumu güncellenemedi:', err);
    this.watchedTitles.add(movie.id);
    this.watchedTitles = new Set(this.watchedTitles);
    this.filterMovies();
  }
}
  }
}
</script>
<style scoped>


.main-container {
  display: flex;
  min-height: 100vh;
  background: #1a1c2c;
  align-items: stretch;
}
.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px 20px;

  /* SABİTLİĞİ VE İÇ SCROLL'U KALDIRAN AYARLAR */
  position: relative;   /* Fixed veya Absolute değil, akışa dahil */
  height: auto;         /* Sabit yükseklik yok */
  min-height: 100vh;    /* En az ekran boyu kadar olsun */
  overflow: visible;    /* İçinde scroll oluşmasını engeller */

  display: flex;
  flex-direction: column;
  z-index: 10;
}

.main-container {
  display: flex;
  align-items: flex-start; /* Sidebar'ın boyunun içeriğe göre uzamasını sağlar */
  min-height: 100vh;
  background: #1a1c2c; /* Arka planın kopmaması için */
}

.logo-area {
  /* Logo alanını üstteki navigasyonun yüksekliğine göre ayarlıyoruz */
  height: 50px; /* Top-nav yüksekliği ile uyumlu */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 40px;
  background: linear-gradient(to right, #fff, #ffcc00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  height: 50px;
}
.side-btn {
  padding: 14px 20px;
  border-radius: 15px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  text-align: left;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
}

.side-btn.active {
  background: #ffcc00;
  color: #1a1c2c;
  font-weight: 700;
}

.content-area {
  flex: 1;
  padding: 40px;
  min-height: 100vh;
}

.search-wrapper {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 25px;
  border-radius: 20px;
  display: flex;
  width: 450px;
}

.search-wrapper input {
  background: transparent;
  border: none;
  color: white;
  width: 100%;
  outline: none;
}

/* KART YENİLİKLERİ */
.titles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 30px;
}

.movie-card {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  transition: transform 0.4s;
}

.movie-card:hover {
  transform: translateY(-10px);
}

.card-image {
  height: 320px;
  position: relative;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background-color: #2a2d3e;
}


.card-top-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
}

.action-btn {
  width: 36px;
  height: 36px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.3s;
}

.action-btn:hover { background: #ffcc00; color: #000; }
.action-btn.active { background: rgba(255, 255, 255, 0.9); }

/* DETAY BUTONU OVERLAY */
.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: 0.3s;
}

.movie-card:hover .card-overlay { opacity: 1; }

.view-btn {
  background: #ffcc00;
  color: #1a1c2c;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

/* ALT DETAYLAR */
.card-details { padding: 15px; }
.title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.title-row h3 { font-size: 15px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.watched-status {
  cursor: pointer;
  color: rgba(255, 255, 255, 0.2);
  font-size: 18px;
  transition: 0.3s;
}

.watched-status.is-watched { color: #4caf50; text-shadow: 0 0 10px rgba(76, 175, 80, 0.5); }

.badge-type {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: #ffcc00;
  color: #1a1c2c;
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 10px;
  z-index: 5;
}

.card-meta { font-size: 12px; color: rgba(255, 255, 255, 0.5); }

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: 0.3s;
  z-index: 8;
  cursor: pointer;
}

.filter-group {
  margin-bottom: 25px;
  max-height: 40vh;
  display: flex;
  flex-direction: column;
}
.filter-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 15px;
  padding-left: 10px;
  font-weight: 600;
}

/* Modern Tab Butonları (Gruplar için) */
.modern-tabs {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modern-tab-btn {
  position: relative;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.6);
  text-align: left;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.modern-tab-btn .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: transparent;
  transition: 0.3s;
}

.modern-tab-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  transform: translateX(5px);
}

.modern-tab-btn.active {
  background: rgba(255, 204, 0, 0.1);
  border-color: rgba(255, 204, 0, 0.3);
  color: #ffcc00;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.modern-tab-btn.active .dot {
  background: #ffcc00;
  box-shadow: 0 0 8px #ffcc00;
}

.genre-cloud {
  overflow-y: auto;
  padding-right: 5px;
}
.genre-chip {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  color: rgba(255, 255, 255, 0.8);
}

.genre-chip:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.05);
}

.genre-chip.active {
  background: #ffcc00;
  color: #1a1c2c;
  border-color: #ffcc00;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(255, 204, 0, 0.3);
}


.sidebar::-webkit-scrollbar {
  display: none;
}
.sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 205, 0, 0.2);
  border-radius: 10px;
}
.movie-card:hover .card-overlay { opacity: 1; }
.view-btn {
  pointer-events: none;
  background: #ffcc00;
  color: #1a1c2c;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 800;
}
.active { color: #ff3366 !important; }
.is-watched { color: #4caf50 !important; }
</style>