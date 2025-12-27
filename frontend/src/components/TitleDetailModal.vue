<template>
  <div v-if="isOpen" class="modal-overlay" @click="close">
    <div class="modal-container" @click.stop>
      <div class="modal-actions">
    <button class="favorite-btn" :class="{ 'active': isFavorited }" @click="toggleFavorite">
      {{ isFavorited ? '❤️' : '🤍' }}
    </button>
    <button class="close-btn" @click="close">✕</button>
  </div>
      <div class="modal-content">
        <div class="poster-section">
          <div class="image-wrapper">
            <img
              :src="title.poster || 'https://via.placeholder.com/300x450?text=No+Poster'"
              :alt="title.title_name"
              class="poster-image"
            />
            <div class="avg-rating-badge">
              ⭐ {{ title.ortalama_puan || '0.0' }}
            </div>
          </div>

          <button @click="markWatched(title.id)"
                 :class="isWatched ? 'watched-active' : 'watched-passive'"
                 class="watched-btn">
            {{ isWatched ? '✓ İzlendi' : 'İzledim İşaretle' }}
          </button>

          <button v-if="!isAddedToWatchlist"
  @click="addToWatchlist"
  class="watchlist-btn">
  📌 İzlenecekler Listesine Ekle
</button>
          <div v-else class="already-in-watchlist">
  <span class="check-mark">✓</span> İzlenecekler Listenizde
</div>

          <div class="cast-info-box">
            <p><strong>🎬 Yönetmen:</strong> {{ title.yonetmen || 'Bilinmiyor' }}</p>
            <p><strong>🎭 Oyuncular:</strong> {{ title.aktorler || 'Bilgi yok' }}</p>
            <p class="imdb-text"><strong>IMDb:</strong> ⭐ {{ title.imdb_rating || 'N/A' }}</p>
          </div>
        </div>

        <div class="info-section">
          <h2 class="title-name">{{ title.title_name }}</h2>
          <div class="meta-info">
            <span class="year">📅 {{ title.yil }}</span>
            <span class="type">🎥 {{ title.cesit }}</span>
            <span class="duration" v-if="title.sure">⏱️ {{ title.sure }} dk</span>
            <span class="imdb-badge" v-if="title.imdb_rating">⭐ IMDb: {{ title.imdb_rating }}</span>
          </div>
          <div class="ozet-section">
             <h3>📝 Özet</h3>
            <p>{{ title.ozet || 'Özet bilgisi bulunmamaktadır.' }}</p>
          </div>
           <div v-if="title.cesit === 'dizi'" class="dizi-detay-info">
           <div v-if="title.sezon_sayisi" class="dizi-stat">
               <strong>Sezon Sayısı:</strong> {{ title.sezon_sayisi }}
               </div>
                <div v-if="title.bolum_sayisi" class="dizi-stat">
                  <strong>Bölüm Sayısı:</strong> {{ title.bolum_sayisi }}
                 </div>
             </div>
<div class="rating-section" v-if="isLoggedIn">
    <h3>⭐ Puan Ver</h3>
    <div class="stars">
      <span v-for="star in 5" :key="star"
            @click="userRating = star"
            :class="{ 'active': star <= userRating }">★</span>
    </div>
            <textarea v-model="userComment" placeholder="Yorumunuzu yazın..."></textarea>
            <button @click="saveReview" class="save-btn">Gönder</button>
          </div>
</div>

          <div v-if="title.fragman_url" class="fragman-section">
            <h3>🎬 Fragman</h3>
            <iframe
              :src="getEmbedUrl(title.fragman_url)"
              width="100%"
              height="200"
              frameborder="0"
              allowfullscreen>
            </iframe>
          </div>
          <div class="reviews-display-section">
  <h3>💬 Kullanıcı Yorumları</h3>

  <div v-if="comments.length > 0" class="comments-list">
    <div v-for="rev in comments" :key="rev.id" class="comment-card">
      <div class="comment-header">
        <span class="user-name">👤 {{ rev.user_name || 'Anonim Kullanıcı' }}</span>
        <span class="user-stars">⭐ {{ rev.rating_value }}/5</span>
      </div>
      <p class="comment-text">{{ rev.yorum }}</p>
    <span class="comment-date">{{ formatDate(rev.yorum_saati || rev.created_at) }}</span>
    </div>
  </div>

  <div v-else class="no-comments">
    Henüz yorum yapılmamış. İlk yorumu sen yap!
  </div>
</div>
        </div>
      </div>
    </div>
</template>

<script>
import apiClient from '@/api/axios'

export default {
  name: "TitleDetailModal",
  props: {
    isOpen: Boolean,
    title: {type: Object, default: () => ({})}
  },
data() {
    return {
      activeSeason: 1,
      episodes: [],
      loadingEpisodes: false,
      isFavorited: false,
      comments: [],
      userRating: 0,
      userComment: '',
      isLoggedIn: !!(localStorage.getItem('token') || localStorage.getItem('authToken')),
      isWatched: false,
      isAddedToWatchlist: false,
    }
  },

  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.comments = [];
        this.checkIfFavorited();
        this.checkWatchlistStatus();
        this.fetchComments();
        if (this.isSeries) {
          this.fetchEpisodes(this.activeSeason);
        }
      }
    },
    activeSeason(newVal) {
      if (this.isOpen && this.isSeries) {
        this.fetchEpisodes(newVal);
      }
    }
  },
  computed: {
    isSeries() {
      const type = (this.title.cesit || '').toLowerCase();
      return type.includes('dizi') || type.includes('series');
    }
  },
  methods: {
    async checkWatchlistStatus() {
    if (!this.isLoggedIn || !this.title.id) return;
    try {
      const res = await apiClient.get('izlenecekler/');
      this.isAddedToWatchlist = res.data.some(item =>
        (item.title === this.title.id) || (item.title_details && item.title_details.id === this.title.id)
      );
    } catch (err) {
      console.error("İzleme listesi durumu kontrol edilemedi:", err);
    }
  },

    close() {
      this.$emit('close');
    },
    getEmbedUrl(url) {
      if (!url) return '';
      let videoId = '';
      if (url.includes('v=')) {
        videoId = url.split('v=')[1].split('&')[0];
      } else if (url.includes('youtu.be/')) {
        videoId = url.split('youtu.be/')[1];
      } else if (url.includes('embed/')) {
        return url;
      }
      return videoId ? `https://www.youtube.com/embed/${videoId}` : url;
    },
    async checkIfFavorited() {
      if (!this.isLoggedIn) return;
      try {
    const res = await apiClient.get('/favoriler/');
    this.isFavorited = res.data.some(fav => fav.title === this.title.id);
  } catch (err) {
    this.isFavorited = false;
  }
},
    async toggleFavorite() {
  if (!this.isLoggedIn) {
    alert("Favorilere eklemek için giriş yapmalısınız.");
    return;
  }
  try {
    const res = await apiClient.post('/toggle-favorite/', { title_id: this.title.id });

    if (res.data.status === 'added') {
      this.isFavorited = true;
    } else {
      this.isFavorited = false;
    }

    console.log(res.data.message);
    this.$emit('toggle-favorite', this.title);

  } catch (err) {
    console.error("Favori işlemi hatası:", err.response?.data);
    const favs = await apiClient.get('/favoriler/');
    const existing = favs.data.find(f => f.title === this.title.id);
    if(existing) {
        await apiClient.delete(`/favoriler/${existing.id}/`);
        this.isFavorited = false;
    }
  }
},

    async fetchComments() {
    if (!this.title || !this.title.id) return;

    try {
      const res = await apiClient.get(`/puanlar/?title=${this.title.id}`);
      this.comments = res.data;
    } catch (err) {
      console.error("Yorumlar yüklenemedi:", err);
      this.comments = [];
    }
  },


async addToWatchlist() {
    if (!this.isLoggedIn) {
      alert("Giriş yapmalısınız.");
      return;
    }
    try {
      await apiClient.post('izlenecekler/', {
        title: this.title.id
      });

      this.isAddedToWatchlist = true;
      this.$emit('status-changed', this.title.id, 'watchlist_added');
      alert("İzlenecekler listesine eklendi!");
    } catch (err) {
      if (err.response?.status === 400) {
        this.isAddedToWatchlist = true;
        alert("Bu içerik zaten listenizde.");
      } else {
        alert("Bir hata oluştu.");
      }
    }
  },
   async saveReview() {
    if (this.userRating === 0) return alert("Lütfen bir puan seçin!");
    try {
      await apiClient.post('/puanlar/', {
        title: this.title.id,
        rating_value: this.userRating,
        yorum: this.userComment
      });
      alert('Yorumunuz gönderildi!');
      this.userComment = '';
      this.userRating = 0;
      this.fetchComments();
    } catch (err) {
      alert('Hata: Puan kaydedilemedi.');
    }
  },
    async toggleWatchlist() {
  if (!this.isLoggedIn) {
    alert("İzleme listesine eklemek için giriş yapmalısınız.");
    return;
  }
  try {

    await apiClient.post('/izleme-listesi/', { title: this.title.id });
    alert("İzleme listesine eklendi!");
  } catch (err) {
    console.error("Liste hatası:", err);
    alert("İzleme listesine eklenirken bir hata oluştu.");
  }
},
    async fetchEpisodes(seasonNumber) {
      this.loadingEpisodes = true;
      try {
        const res = await apiClient.get(`titles/${this.title.id}/season/${seasonNumber}/`);
        this.episodes = res.data;
      } catch (e) {
        console.error("Bölümler yüklenemedi");
      } finally {
        this.loadingEpisodes = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('tr-TR');
    },
   async markWatched(id) {
  if (!this.isLoggedIn) return alert("Giriş yapmalısınız.");
  try {

    await apiClient.post('izleme-gecmisi/', { title: id });

    this.isWatched = true;

    this.$emit('status-changed', id, 'watched');

    alert("İzleme geçmişine eklendi.");
    this.close();
  } catch (err) {
    console.error("İzleme kaydedilemedi:", err);
    alert("Bir hata oluştu.");
  }
},
  }
}
</script>

<style scoped>

.modal-actions {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 10px;
  z-index: 10002;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-container {
  background: linear-gradient(135deg, #1e2a5a, #2d1b5a); /* Daha modern ve koyu bir ton */
  border-radius: 16px;
  max-width: 950px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Grid Yapısı  */
.modal-content {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 30px;
  padding: 30px;
  color: white;
}

/* Sol Kolon: Poster ve Künye */
.poster-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.image-wrapper {
  position: relative;
  width: 100%;
}

.poster-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.watchlist-btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  border: 2px solid #ffcc00;
  background: transparent;
  color: #ffcc00;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}
.watchlist-btn:hover {
  background: #ffcc00;
  color: #000;
}
.watched-active { background: #28a745; color: white; }
.watched-passive { background: #444; color: white; }

.cast-info-box {
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.6;
}
.cast-info-box p { margin: 5px 0; color: #eee; }
.imdb-text { color: #ffcc00 !important; font-weight: bold; }


.info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.imdb-badge {
  background: #f5c518 !important;
  color: #000 !important;
  font-weight: bold;
}

.dizi-detay-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  font-size: 15px;
}
.dizi-stat {
  color: #eee;
}
.dizi-stat strong {
  color: #ffcc00;
  margin-right: 5px;
}
.title-name {
  font-size: 32px;
  margin: 0;
  font-weight: bold;
  color: #ffcc00;
}

.meta-info {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.meta-info span {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  font-size: 13px;
}

.ozet-section, .fragman-section, .rating-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.stars { font-size: 24px; margin-bottom: 10px; }
.stars span { cursor: pointer; color: #555; transition: 0.2s; }
.stars span.active { color: #ffcc00; }

textarea {
  width: 100%;
  height: 80px;
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  color: white;
  padding: 10px;
  border-radius: 8px;
  resize: none;
}

.close-btn {
  position: static; /* Grupta yan yana gelmesi için */
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: 0.3s;
}
.close-btn:hover {
  background: rgba(255, 0, 0, 0.6);
}

.favorite-btn {
  position: static;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  font-size: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, background 0.3s;
}
.favorite-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.favorite-btn.active {
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
}

.dizi-detay-row .form-group {
  flex: 1;
}
.reviews-display-section {
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
}

.comments-list {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-card {
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.85rem;
}

.user-name {
  font-weight: bold;
  color: #ffcc00;
}

.comment-text {
  font-size: 0.9rem;
  color: #eee;
  line-height: 1.4;
  margin: 5px 0;
}

.comment-date {
  font-size: 0.7rem;
  color: #888;
  display: block;
  text-align: right;
}

.no-comments {
  text-align: center;
  color: #888;
  padding: 20px;
}

@media (max-width: 768px) {
  .modal-content {
    grid-template-columns: 1fr;
    padding: 20px;
  }
  .poster-image {
    max-width: 200px;
    margin: 0 auto;
  }
}
/* Sezonlar ve Bölümler Konteynırı */
.seasons-container {
  margin-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
}

/* Sezon Tabları */
.season-tabs {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.season-tab {
  background: transparent;
  border: none;
  color: #888;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  padding: 5px 0;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.season-tab.active {
  color: #ffcc00;
  border-bottom-color: #ffcc00;
}

/* Bölüm Kartı */
.episode-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px;
  border-radius: 12px;
  transition: background 0.3s;
  cursor: pointer;
  margin-bottom: 10px;
}

.episode-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.ep-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: #444;
  min-width: 30px;
}

.ep-thumbnail {
  position: relative;
  width: 160px;
  aspect-ratio: 16/9;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.ep-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ep-play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: 0.3s;
}

.episode-item:hover .ep-play-overlay {
  opacity: 1;
}

/* Bölüm Bilgisi */
.ep-info {
  flex: 1;
}

.ep-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.ep-title-row h4 {
  margin: 0;
  font-size: 1rem;
  color: #fff;
}

.ep-runtime {
  font-size: 0.8rem;
  color: #888;
}

.ep-overview {
  font-size: 0.85rem;
  color: #aaa;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 12px;
}
.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.watchlist-btn {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  border-radius: 8px;
  border: 2px solid #ffcc00;
  background: transparent;
  color: #ffcc00;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.watchlist-btn:hover {
  background: rgba(255, 204, 0, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 204, 0, 0.2);
}

.watchlist-btn:active {
  transform: scale(0.98);
}
.already-in-watchlist {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.3);
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: default;
}

.check-mark {
  font-size: 18px;
}
</style>

