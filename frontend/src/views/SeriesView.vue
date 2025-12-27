<template>
  <div class="main-container">
    <aside class="sidebar">
      <div class="logo-area">
        <span class="logo-icon">📺</span>
        <h2 class="logo-text">Diziler</h2>
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
            @click="selectedGenres = []; fetchSeries()"
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
            placeholder="Dizi ara..."
            @input="filterSeries"
          />
        </div>
        <div class="user-stats">
          <span>{{ filteredSeries.length }} dizi bulundu</span>
        </div>
      </header>

      <section class="movies-explorer">
        <div v-if="loadingSeries" class="loader-container">
          <div class="spinner"></div>
          <p>Dizi kütüphanesi taranıyor...</p>
        </div>

        <div v-else-if="seriesError" class="error-msg">{{ seriesError }}</div>

        <div v-else-if="filteredSeries.length > 0" class="titles-grid">
          <div
            v-for="(serie, index) in filteredSeries"
            :key="serie.id"
            class="movie-card"
            :style="{ '--delay': index }"
          >
            <div class="card-image">
              <img
                :src="serie.poster || 'https://via.placeholder.com/280x400?text=No+Poster'"
                @error="(e) => e.target.src = 'https://via.placeholder.com/280x400?text=No+Poster'"
                class="poster-img"
                alt="dizi posteri"
              >

              <div class="card-badges">
                <span class="badge-type">{{ serie.cesit || 'Dizi' }}</span>
              </div>

              <div class="card-top-actions">
                <div class="action-btn fav-btn" @click.stop="toggleFavorite(serie)" :class="{ 'active': favoritedTitles.has(serie.id) }">
                  {{ favoritedTitles.has(serie.id) ? '❤️' : '🤍' }}
                </div>
              </div>

              <div class="card-overlay" @click.stop="viewDetails(serie.id)">
                <button class="view-btn">Detayları Gör</button>
              </div>
            </div>

            <div class="card-details">
              <div class="title-row">
                <h3>{{ serie.title_name }}</h3>
              </div>
              <div class="card-meta">
                <span class="m-year">{{ serie.yil }}</span>
                <span class="m-dot">•</span>
                <span class="m-duration" v-if="serie.sure">{{ serie.sure }} dk</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>😔 Aradığınız kriterlere uygun dizi bulunamadı.</p>
        </div>
      </section>
    </main>

    <TitleDetailModal
  v-if="showModal"
  :isOpen="showModal"
  :title="selectedTitle || {}"
  @close="closeModal"
  @status-changed="handleStatusChange"
/>
  </div>
</template>

<script>
import apiClient from '@/api/axios'
import TitleDetailModal from '@/components/TitleDetailModal.vue'

export default {
  name: 'SeriesView',
  components: {
    TitleDetailModal
  },
  data() {
    return {
      allSeries: [],
      allGenres: [],
      loadingSeries: false,
      seriesError: null,
      searchQuery: '',
      selectedGroup: 'genel',
      selectedGenres: [],
      selectedTitle: null,
      showModal: false,
      favoritedTitles: new Set(),
      watchedTitles: new Set(),
      groups: [
        { id: 'genel', label: 'Genel' },
        { id: 'anime', label: 'Animeler' },
        { id: 'kore', label: 'Kore Dizileri' }
      ]
    }
  },
  computed: {
    filteredSeries() {
      let list = this.allSeries;
      list = list.filter(item => !this.watchedTitles.has(item.id));
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        list = list.filter(serie =>
          (serie.title_name && serie.title_name.toLowerCase().includes(query)) ||
          (serie.ozet && serie.ozet.toLowerCase().includes(query))
        );
      }
      return this.allSeries.filter(item => !this.watchedTitles.has(item.id));
    }
  },
  async mounted() {
    const token = localStorage.getItem('authToken') || localStorage.getItem('token')
    if (!token) {
      this.$router.push('/login')
      return
    }
    await this.fetchGenres();
    await this.fetchWatchedList();
    await this.fetchSeries();
    await this.fetchFavorites();
  },
  methods: {
    async fetchWatchedList() {
      try {
        const res = await apiClient.get('izleme-gecmisi/')
        this.watchedTitles = new Set(res.data.map(item => item.title));
      } catch (err) {
        console.error("İzlenenler listesi alınamadı:", err);
      }
    },
    async fetchSeries() {
      try {
        this.loadingSeries = true;
        const response = await apiClient.get('titles/', {
          params: {
            grup: this.selectedGroup,
            kategori: this.selectedGenres.join(',') || undefined
          }
        });

        this.allSeries = response.data
          .filter(t => {
            const type = (t.cesit || '').toLowerCase();
            return type.includes('dizi') || type.includes('series');
          })
          .sort((a, b) => b.yil - a.yil);

      } catch (err) {
        this.seriesError = 'Diziler yüklenemedi';
      } finally {
        this.loadingSeries = false;
      }
    },
    handleStatusChange(id, status) {
      if (status === 'watched') {
        this.watchedTitles.add(id);
        this.watchedTitles = new Set(this.watchedTitles);
      }
    },

    async fetchGenres() {
      try {
        const response = await apiClient.get('turler/')
        this.allGenres = response.data
      } catch (err) {
        console.error("Türler yüklenemedi:", err)
      }
    },
    changeGroup(groupId) {
      this.selectedGroup = groupId
      this.selectedGenres = []
      this.fetchSeries()
    },
    toggleGenre(genreTitle) {
      const index = this.selectedGenres.indexOf(genreTitle)
      if (index > -1) {
        this.selectedGenres.splice(index, 1)
      } else {
        this.selectedGenres.push(genreTitle)
      }
      this.fetchSeries()
    },
    viewDetails(serieId) {
      const serie = this.allSeries.find(s => s.id === serieId)
      if (serie) {
        this.selectedTitle = serie
        this.showModal = true
      }
    },
    closeModal() {
      this.showModal = false
      this.selectedTitle = null
    },
    async fetchFavorites() {
      try {
        const response = await apiClient.get('favoriler/')
        this.favoritedTitles = new Set(response.data.map(fav => fav.title))
      } catch (err) {
        console.error('Fetch favorites error:', err)
      }
    },
    async toggleFavorite(serie) {
      try {
        const token = localStorage.getItem('authToken') || localStorage.getItem('token')
        if (!token) return this.$router.push('/login')

        const response = await apiClient.get('favoriler/')
        const favId = response.data.find(fav => fav.title === serie.id)?.id

        if (favId) {
          await apiClient.delete(`favoriler/${favId}/`)
          this.favoritedTitles.delete(serie.id)
        } else {
          await apiClient.post('favoriler/', { title: serie.id })
          this.favoritedTitles.add(serie.id)
        }
        this.favoritedTitles = new Set(this.favoritedTitles)
      } catch (err) {
        console.error('Favorite error:', err)
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
  color: white;
  font-family: 'Poppins', sans-serif;
}

.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.content-area {
  flex: 1;
  padding: 40px;
  min-height: 100vh;
}

.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  margin-bottom: 30px;
  background: linear-gradient(to right, #fff, #ffcc00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  height: 60px;
}

.search-wrapper {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 25px;
  border-radius: 20px;
  display: flex;
  width: 450px;
  backdrop-filter: blur(5px);
}

.search-wrapper input {
  background: transparent;
  border: none;
  color: white;
  width: 100%;
  outline: none;
  margin-left: 10px;
}

/* Kategori Butonları */
.modern-tabs { display: flex; flex-direction: column; gap: 8px; }
.modern-tab-btn {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 10px;
}
.modern-tab-btn.active {
  background: rgba(255, 204, 0, 0.1);
  border-color: rgba(255, 204, 0, 0.3);
  color: #ffcc00;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: transparent; }
.active .dot { background: #ffcc00; box-shadow: 0 0 8px #ffcc00; }


.titles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 30px;
}
.movie-card {
  position: relative;
  border-radius: 16px;
  background: #25283b;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.movie-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 30px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 204, 0, 0.4);
}
.card-image {
  position: relative;
  aspect-ratio: 2/3;
  height: auto;
  overflow: hidden;
}
.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
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
}
.movie-card:hover .poster-img {
  transform: scale(1.1);
}
.movie-card:hover .card-overlay { opacity: 1; }
.badge-type {
  background: rgba(255, 204, 0, 0.9);
  color: #000;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
.card-top-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
}

.movie-card:hover .card-top-actions {
  opacity: 1;
  transform: translateX(0);
}

.action-btn {
  width: 34px;
  height: 34px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26, 28, 44, 0.9) 0%, rgba(26, 28, 44, 0.2) 60%, transparent 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
}

.movie-card:hover .card-overlay {
  opacity: 1;
}

.view-btn {
  background: #ffcc00;
  color: #000;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 700;
  font-size: 13px;
  transform: translateY(20px);
  transition: all 0.4s ease;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(255, 204, 0, 0.4);
}

.movie-card:hover .view-btn {
  transform: translateY(0);
}

.card-details {
  padding: 15px;
  background: #25283b;
}

.title-row h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #efefef;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #9ca3af;
}

.m-year {
  color: #ffcc00;
  font-weight: 500;
}
.action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.genre-cloud { display: flex; flex-wrap: wrap; gap: 8px; }
.genre-chip {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
}
.genre-chip.active { background: #ffcc00; color: #1a1c2c; }

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
  width: 36px; height: 36px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  display: flex;
  align-items: center; justify-content: center;
  cursor: pointer;
}
.watched-status.is-watched { color: #4caf50 !important; }

/* Loader */
.loader-container { text-align: center; padding: 50px; }
.spinner {
  width: 40px; height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: #ffcc00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>

