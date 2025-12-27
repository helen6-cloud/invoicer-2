<template>
  <div class="favorites-page">
    <h2 class="page-title">❤️ Favorilerim</h2>

    <div v-if="loading" class="loading">Favorileriniz getiriliyor...</div>

    <div v-else-if="favorites && favorites.length > 0" class="titles-grid">
      <div
        v-for="item in favorites"
        :key="item.id"
        class="title-card"
        :style="{ backgroundImage: `url(${item.title_details?.poster || item.poster || 'https://via.placeholder.com/280x400'})` }"
      >
        <div class="favorite-star" @click.stop="removeFavorite(item.id)">❤️</div>

        <div class="title-overlay">
          <div class="title-header">
            <h4>{{ item.title_details?.title_name || item.title_name }}</h4>
          </div>

          <div class="title-info">
            <p class="ozet">
              {{ item.title_details?.ozet ? item.title_details.ozet.substring(0, 60) + '...' : 'Özet yok' }}
            </p>
          </div>

          <button class="action-btn" @click="viewDetails(item.title_details || item)">
            Detaylı Gör
          </button>
        </div> </div> </div> <div v-else class="no-favorites animate-fade">
      <p>😔 Henüz favori listenize bir içerik eklemediniz.</p>
    </div>

    <TitleDetailModal
      v-if="showModal"
      :isOpen="showModal"
      :title="selectedTitle || {}"
      :favoritedTitles="new Set(favorites.map(f => f.title))"
      @close="closeModal"
    />
  </div>
</template>

<script>
import apiClient from '@/api/axios'; // axios instance'ınızın doğru yolu
import TitleDetailModal from '@/components/TitleDetailModal.vue';

export default {
  name: "FavoritesView",
  components: { TitleDetailModal },
  data() {
    return {
      favorites: [], // data içindeki isim favorites olarak güncellendi
      loading: false,
      showModal: false,
      selectedTitle: null,
      userToken: localStorage.getItem('token') || localStorage.getItem('authToken'),
    };
  },
  mounted() {
    if (!this.userToken) {
      this.$router.push('/login');
      return;
    }
    this.fetchFavorites();
  },
  methods: {
    async fetchFavorites() {
      try {
    this.loading = true;
    const response = await apiClient.get('/favoriler/');

    console.log("Backendden gelen veri:", response.data);

    this.favorites = response.data;
  } catch (err) {
    console.error("Favori yükleme hatası:", err);
  } finally {
    this.loading = false;
  }
},

    async removeFavorite(favId) {
      try {
        await apiClient.delete(`/favoriler/${favId}/`, {
          headers: { Authorization: `Token ${this.userToken}` }
        });
        // Listeyi anında güncelle
        this.favorites = this.favorites.filter(f => f.id !== favId);
      } catch (err) {
        console.error("Kaldırma hatası:", err);
        alert("Favori kaldırılırken bir hata oluştu.");
      }
    },

    viewDetails(titleObj) {
      this.selectedTitle = titleObj;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedTitle = null;
    }
  },
};
</script>

<style scoped>
.favorites-page {
  padding: 80px 40px 40px;
  min-height: 100vh;
  background: #141414;
  color: white;
}

.page-title {
  font-size: 32px;
  margin-bottom: 30px;
  text-align: center;
}

.titles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 25px;
  max-width: 1200px;
  margin: 0 auto;
}

.title-card {
  height: 380px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.title-card:hover {
  transform: translateY(-10px);
}

.title-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 30%, rgba(0,0,0,0.9));
}

.favorite-star {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10;
  cursor: pointer;
  font-size: 24px;
  filter: drop-shadow(0 0 5px rgba(0,0,0,0.5));
}

.title-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px;
  z-index: 5;
}

.title-header h4 {
  margin: 0;
  font-size: 18px;
}

.year {
  font-size: 12px;
  color: #ffcc00;
}

.title-info .ozet {
  font-size: 12px;
  color: #ccc;
  margin: 10px 0;
}

.action-btn {
  width: 100%;
  padding: 8px;
  background: #ffcc00;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.no-favorites {
  text-align: center;
  margin-top: 100px;
  font-size: 20px;
  color: #888;
}

.loading {
  text-align: center;
  margin-top: 50px;
}

.animate-fade {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>