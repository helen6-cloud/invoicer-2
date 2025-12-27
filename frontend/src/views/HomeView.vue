<template>
  <div class="home-wrapper">
    <div class="layout-container">
      <aside class="sidebar-filters animate-fade-in">
        <h2 class="sidebar-title">Filtrele</h2>

        <div class="filter-group">
          <h3>Tür</h3>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterType" value="film">
            <span class="checkmark"></span> 🎬 Film
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="filterType" value="dizi">
            <span class="checkmark"></span> 📺 Dizi
          </label>
        </div>

        <div class="filter-group">
          <h3>Özel</h3>
          <label class="checkbox-label">
            <input type="checkbox" v-model="isTurkish">
            <span class="checkmark"></span> 🇹🇷 Yerli Yapım
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="isAnime">
            <span class="checkmark"></span> ⛩️ Anime
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="isKorean">
            <span class="checkmark"></span> Kore Dizisi
          </label>
        </div>

        <div class="filter-group">
          <h3>Kategoriler</h3>
          <div class="category-scroll-list">
            <label v-for="cat in kategoriler" :key="cat.id" class="checkbox-label">
              <input type="checkbox" v-model="selectedCategories" :value="cat.baslik">
              <span class="checkmark"></span>
              {{ cat.baslik }}
            </label>
          </div>
        </div>

        <button v-if="hasActiveFilters" @click="resetFilters" class="reset-btn">
          Filtreleri Temizle
        </button>
      </aside>
      <main class="content-area">
        <div class="header-section animate-fade-in">
          <h1 class="title">Film & Dizi</h1>
          <p class="subtitle">Keyfine göre öneriler keşfet ve izle!</p>
        </div>

        <div v-if="searchQuery" class="search-results animate-fade-in">
           <h2 class="section-title">🔍 "{{ searchQuery }}" Sonuçları</h2>
           <div class="titles-grid-search">
             <div v-for="item in filteredResults" :key="item.id" class="title-card" @click="viewDetails(item.id)">
                <img
  :src="item.poster_url || 'https://via.placeholder.com/300x450?text=Resim+Yok'"
  @error="(e) => e.target.src = 'https://via.placeholder.com/300x450?text=Resim+Yok'"
  class="card-img"
>
                <div class="title-overlay">
                  <h4>{{ item.title_name }}</h4>
                </div>
             </div>
           </div>
           <div v-if="filteredResults.length === 0" class="no-results">Sonuç bulunamadı...</div>
        </div>

        <div v-if="!searchQuery && !hasActiveFilters">
          <section v-if="featuredTitles.length > 0" class="mb-12 animate-fade-in">
            <h2 class="section-title">🔥 Sizin İçin Seçtiklerimiz</h2>
            <div class="slider-container">
              <div class="slider-track">
                <div v-for="title in featuredTitles" :key="'feat-'+title.id" class="slider-item featured-item" @click="viewDetails(title.id)">
                  <img :src="title.poster_url || 'https://via.placeholder.com/300x170'" :alt="title.title_name">
                  <div class="item-info">
                    <h3>{{ title.title_name }}</h3>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section v-if="isLoggedIn && smartRecommendations.length > 0" class="mb-12 animate-fade-in delay-1">
            <h2 class="section-title">✨ Sana Özel Öneriler</h2>
            <div class="slider-container">
              <div class="slider-track">
                <div v-for="item in smartRecommendations" :key="'smart-'+item.id" class="slider-item" @click="viewDetails(item.id)">
                  <img :src="item.poster_url || 'https://via.placeholder.com/300x450'" :alt="item.title_name">
                  <div class="item-info">
                    <h3>{{ item.title_name }}</h3>
                    <span>{{ item.imdb_rating ? '⭐ '+item.imdb_rating : '' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <div v-if="loading" class="text-center py-10">Yükleniyor...</div>

          <div v-else>
          <section v-for="(kat, index) in filteredKategorizeVeriler" :key="index" class="category-row animate-up">
  <h2 class="section-title">{{ kat.kategori_adi }}</h2>

  <div class="slider-wrapper">
    <button
  class="nav-arrow left"
  :class="{ hidden: !canScrollLeft[index] }"
  @click="scrollSlider(index, 'left')">

      <span class="arrow-icon">❮</span>
    </button>

    <div class="slider-container" :ref="'slider-' + index">
      <div class="slider-track">
        <div v-for="item in kat.icerikler" :key="item.id" class="slider-item" @click="viewDetails(item.id)">
          <img :src="item.poster_url || 'https://via.placeholder.com/300x450'" loading="lazy">
          <div class="item-hover-overlay">
            <button class="play-btn">▶</button>
            <h4>{{ item.title_name }}</h4>
            <div class="meta">
              <span>{{ item.yil }}</span>
              <span class="hd-badge">4K</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button
  class="nav-arrow right"
  :class="{ hidden: !canScrollRight[index] }"
  @click="scrollSlider(index, 'right')">

      <span class="arrow-icon">❯</span>
    </button>
  </div>
</section>

            <div v-if="filteredKategorizeVeriler.length === 0" class="no-results py-10">
              Seçilen filtrelere uygun içerik bulunamadı.
            </div>
          </div>
        </div>
      </main>
    </div>

    <TitleDetailModal
  v-if="showModal"
  :isOpen.sync="showModal"
  :title="selectedTitle"
  @close="showModal = false"
  :favoritedTitles="favoritedTitles"
  @favorite-updated="fetchFavorites"
  @toggle-favorite="toggleFavorite"
  @toggle-watchlist="toggleWatchlist"
  @status-changed="handleStatusChange"
/>
  </div>
</template>

<script>
import TitleDetailModal from '@/components/TitleDetailModal.vue'
import axios from 'axios';

const apiClient = axios.create({ baseURL: 'http://127.0.0.1:8000/api' });

export default {
  name: 'HomeView',
  components: { TitleDetailModal },
  data() {
    return {
      allTitles: [],
      canScrollLeft: {},
      canScrollRight: {},
      featuredTitles: [],
      kategorizeVeriler: [],
      kategoriler: [],
      filterType: [],
      selectedCategories: [],
      isTurkish: false,
      isAnime: false,
      isKorean: false,
      searchQuery: '',
      loading: true,
      showModal: false,
      selectedTitle: null,
      favorites: [],
      favoritedTitles: new Set(),
      watchlistTitles: new Set(),
      userToken: localStorage.getItem('token') || localStorage.getItem('authToken'),
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.userToken && this.userToken !== "null";
    },
    hasActiveFilters() {
      return (
        this.filterType.length > 0 ||
        this.selectedCategories.length > 0 ||
        this.isTurkish ||
        this.isAnime ||
        this.isKorean
      );
    },
    filteredResults() {
      if (!this.searchQuery) return [];
      const query = this.searchQuery.toLowerCase().trim();
      return this.allTitles.filter(t => t.title_name && t.title_name.toLowerCase().includes(query));
    },
    smartRecommendations() {
      if (!this.isLoggedIn || this.allTitles.length === 0) {
        return [...this.allTitles]
          .sort((a, b) => (b.ortalama_puan || 0) - (a.ortalama_puan || 0))
          .slice(0, 6);
      }
      const lovedGenres = new Set();
      this.favorites.forEach(fav => {
        if (fav.title_details && fav.title_details.turler) {
          fav.title_details.turler.forEach(t => lovedGenres.add(t.baslik));
        }
      });

      let candidates = this.allTitles.filter(item => !this.watchlistTitles.has(item.id));
      const scoredCandidates = candidates.map(item => {
        let score = 0;
        if (item.turler) {
          item.turler.forEach(t => { if (lovedGenres.has(t.baslik)) score += 10; });
        }
        score += (parseFloat(item.imdb_rating) || 0);
        if (this.isTurkish && item.is_turkish) score += 5;
        return { ...item, recommendationScore: score };
      });

      return scoredCandidates.sort((a, b) => b.recommendationScore - a.recommendationScore).slice(0, 6);
    },
    filteredKategorizeVeriler() {
      if (!this.kategorizeVeriler) return [];
      return this.kategorizeVeriler
        .map(kat => {
          const yeniKat = { ...kat };
          yeniKat.icerikler = kat.icerikler.filter(item => {
            if (this.watchlistTitles.has(item.id)) return false;
            const itemCesit = (item.cesit || '').toLowerCase();
            const typeMatch = this.filterType.length === 0 || this.filterType.includes(itemCesit);
            const turkishMatch = !this.isTurkish || item.is_turkish;
            const animeMatch = !this.isAnime || item.is_anime;
            const koreanMatch = !this.isKorean || (item.is_korean || item.origin_country === 'KR');
            const categoryMatch = this.selectedCategories.length === 0 || this.selectedCategories.includes(kat.kategori_adi);
            return typeMatch && turkishMatch && animeMatch && koreanMatch && categoryMatch;
          });
          return yeniKat;
        })
        .filter(kat => kat.icerikler.length > 0);
    },
  },
  async mounted() {
    this.loading = true;
    try {
      await Promise.all([
        this.fetchAllTitles(),
        this.fetchCategories(),
        this.fetchKategorizeVeriler(),
        this.fetchFeaturedTitles()
      ]);
      if (this.isLoggedIn) {
        await this.fetchFavorites();
        await this.fetchWatchlist();
      }
    } catch (e) {
      console.error("Yükleme hatası:", e);
    } finally {
      this.loading = false;
    }
    this.$nextTick(() => {
      this.updateScrollButtons();
    });
  },
  methods: {
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    handleStatusChange(id, status) {
      if (status === 'watched' || status === 'watchlist_added') {
        this.watchlistTitles.add(id);
        this.watchlistTitles = new Set(this.watchlistTitles);
      }
    },
    updateScrollButtons() {
      Object.keys(this.$refs).forEach((key) => {
        if (key.startsWith('slider-')) {
          const el = this.$refs[key][0];
          if (el) {
            const index = key.split('-')[1];
            this.canScrollLeft[index] = el.scrollLeft > 0;
            this.canScrollRight[index] = el.scrollLeft + el.clientWidth < el.scrollWidth;
          }
        }
      });
    },
    scrollSlider(index, direction) {
      const container = this.$refs['slider-' + index][0];
      const scrollAmount = 216; // cardWidth + gap
      container.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
      setTimeout(() => this.updateScrollButtons(), 400);
    },
    getHeaders() {
      return { Authorization: `Token ${this.userToken}` };
    },
    async fetchAllTitles() {
      try {
        const res = await apiClient.get('/titles/');
        this.allTitles = res.data;
      } catch (e) {
        console.error("AllTitles error", e);
      }
    },
    async fetchCategories() {
      try {
        const res = await apiClient.get('/turler/');
        this.kategoriler = res.data;
      } catch (e) {
        console.error("Kategoriler hatası", e);
      }
    },
    async fetchKategorizeVeriler() {
      try {
        const res = await apiClient.get('/titles-by-genre/');
        this.kategorizeVeriler = res.data.map(kat => ({
          ...kat,
          icerikler: this.shuffleArray([...kat.icerikler])
        }));
      } catch (e) {
        console.error("Veri çekme hatası:", e);
      }
    },
    async fetchFeaturedTitles() {
      try {
        const res = await apiClient.get('/titles/');
        this.featuredTitles = this.shuffleArray([...res.data]).slice(0, 6);
      } catch (e) {
        console.error(e);
      }
    },
    async fetchFavorites() {
      try {
        const res = await apiClient.get('/favoriler/', { headers: this.getHeaders() });
        this.favorites = res.data;
        this.favoritedTitles = new Set(res.data.map(f => f.title));
      } catch (e) {
        console.error("Fav error", e);
      }
    },
    async fetchWatchlist() {
      try {
        const res = await apiClient.get('/izlenecekler/', { headers: this.getHeaders() });
        this.watchlistTitles = new Set(res.data.map(w => w.title));
      } catch (e) {
        console.warn("Watchlist error");
      }
    },
    async toggleFavorite(item) {
      if (!this.isLoggedIn) return this.$router.push('/login');
      try {
        const resFavs = await apiClient.get('/favoriler/', { headers: this.getHeaders() });
        const existing = resFavs.data.find(f => f.title === item.id);
        if (existing) {
          await apiClient.delete(`/favoriler/${existing.id}/`, { headers: this.getHeaders() });
          this.favoritedTitles.delete(item.id);
        } else {
          await apiClient.post('/favoriler/', { title: item.id }, { headers: this.getHeaders() });
          this.favoritedTitles.add(item.id);
        }
        this.favoritedTitles = new Set(this.favoritedTitles);
      } catch (e) {
        console.error(e);
      }
    },
    toggleWatchlist(item) {
      if (this.watchlistTitles.has(item.id)) this.watchlistTitles.delete(item.id);
      else this.watchlistTitles.add(item.id);
      this.watchlistTitles = new Set(this.watchlistTitles);
    },
    viewDetails(id) {
      let title = this.allTitles.find(t => t.id === id);
      if (!title && this.kategorizeVeriler) {
        this.kategorizeVeriler.forEach(kat => {
          const found = kat.icerikler.find(i => i.id === id);
          if (found) title = found;
        });
      }
      if (title) {
        this.selectedTitle = title;
        this.showModal = true;
      }
    },
    resetFilters() {
      this.filterType = [];
      this.selectedCategories = [];
      this.isTurkish = false;
      this.isAnime = false;
      this.isKorean = false;
    },
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>
<style scoped>
html, body {
  overflow: hidden;
}
.home-wrapper {
  min-height: 100vh;
  background: #0a0a0b;
  color: white;
  overflow-x: hidden;
}
:deep(.modal-overlay) {
  z-index: 9999 !important;
}
.layout-container {
  display: flex;
  align-items: flex-start;
}


.sidebar-filters {
  width: 280px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 30px 20px;
  margin-right: 20px;
  position: relative;
  height: fit-content;
  z-index: 5;
  transition: transform 0.3s ease;
  max-height: calc(100vh - 40px);
}
.sidebar-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #ffcc00;
  border-bottom: 2px solid #ffcc00;
  display: inline-block;
  padding-bottom: 5px;
}

.filter-group {
  margin-bottom: 30px;
}

.filter-group h3 {
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

/* Custom Checkbox Tasarımı */
.checkbox-label {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 0.95rem;
  color: #ddd;
  transition: color 0.2s;
}

.checkbox-label:hover {
  color: white;
}

.checkbox-label input {
  display: none; /* Varsayılanı gizle */
}

.checkmark {
  width: 18px;
  height: 18px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  transition: all 0.2s;
}

.checkbox-label input:checked ~ .checkmark {
  background-color: #ffcc00;
  border-color: #ffcc00;
}

.checkbox-label input:checked ~ .checkmark::after {
  content: '✔';
  position: absolute;
  font-size: 12px;
  color: black;
  top: -1px;
  left: 3px;
}

.sidebar-filters::-webkit-scrollbar, .category-scroll-list::-webkit-scrollbar {
  width: 6px;
}
.sidebar-filters::-webkit-scrollbar-thumb, .category-scroll-list::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 3px;
}

.reset-btn {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: 1px solid #ff4444;
  color: #ff4444;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}
.reset-btn:hover {
  background: #ff4444;
  color: white;
}


.content-area {
  flex: 1;
  padding: 40px;
  margin-left: 0;
  width: auto;
}



.header-section {
  margin-bottom: 40px;
  padding-left: 10px;
}

.title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 10px;
}

.subtitle {
  color: #aaa;
  font-size: 1.1rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  margin-left: 0;
  padding-left: 0;
  border-left: 4px solid #ffcc00;
  display: flex;
  align-items: center;
}

.slider-track {
  display: flex;
  gap: 16px;
  align-items: stretch;
}


.slider-track::-webkit-scrollbar-thumb {
  background: #ffcc00;
  border-radius: 10px;
}

.slider-track::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.slider-container {
  overflow: hidden;
    width: 100%;
}

.slider-track::-webkit-scrollbar {
  height: 4px;
  display: block;
}

.featured-item {
  width: 300px;
  height: 170px;
}

.slider-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
}


/* Hover Efekti */
.slider-item:hover {
  transform: scale(1.05);
  z-index: 5;
}

.item-hover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, black, transparent);
  padding: 15px;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 0 0 8px 8px;
}

.slider-item:hover .item-hover-overlay {
  opacity: 1;
}

.item-hover-overlay h4 {
  font-size: 0.9rem;
  margin: 5px 0;
  font-weight: bold;
}

.meta {
  font-size: 0.75rem;
  color: #ccc;
  display: flex;
  align-items: center;
  gap: 10px;
}

.hd-badge {
  border: 1px solid #ccc;
  padding: 1px 4px;
  font-size: 0.6rem;
  border-radius: 3px;
}

.card-badges {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.6);
  padding: 5px;
  border-radius: 50%;
  z-index: 5;
}

/* Animasyonlar */
.animate-fade-in {
  animation: fadeIn 0.8s ease forwards;
}

.animate-up {
  opacity: 0;
  animation: slideUp 0.8s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 768px) {
  .layout-container {
    flex-direction: column;
  }
  .sidebar-filters {
    width: 100%;
    height: auto;
    position: relative;
    padding: 20px;
    border-right: none;
    border-bottom: 1px solid #333;
  }

  .title { font-size: 2rem; }

}
.sidebar-footer {
  margin-top: auto; /* En alta iter */
  padding-top: 20px;
  padding-bottom: 20px;
}

.logout-btn {
  width: 100%;
  padding: 12px;
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid #ff4444;
  color: #ff4444;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
}

.logout-btn:hover {
  background: #ff4444;
  color: white;
}

.slider-wrapper {
  position: relative;
  width: 100%;
  padding: 10px 0;
}


.slider-container {
  overflow: hidden;
}

.slider-container::-webkit-scrollbar {
  display: none;
}

.nav-arrow {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 50px;
  border: none;
  z-index: 10;
}

.nav-arrow.left {
  left: 0;
}

.nav-arrow.right {
  right: 0;
}

.nav-arrow.hidden {
  display: none;
}

.slider-wrapper:hover .nav-arrow {
  opacity: 1;
}


.arrow-icon {
  font-size: 2.5rem;
  text-shadow: 0 0 10px rgba(0,0,0,0.5);
  transition: transform 0.2s;
}

.nav-arrow:hover .arrow-icon {
  transform: scale(1.3);
  color: white;
}

.slider-item {
  flex: 0 0 180px;
  height: 270px;
  border-radius: 10px;
  overflow: hidden;
  background: #111;
}




@media (max-width: 768px) {
  .slider-item {
    flex: 0 0 140px;
    height: 210px;
  }
}

</style>