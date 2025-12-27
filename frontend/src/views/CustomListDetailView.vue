<template>
  <div class="list-detail-wrapper">
    <div class="header-container">
      <button @click="$router.back()" class="back-btn">← Geri Dön</button>
      <div class="list-info-text">
        <h1 class="page-title">📁 {{ listInfo.isim }}</h1>
        <span class="result-count">{{ contents.length }} içerik</span>
      </div>
    </div>

    <div v-if="loading" class="loading">Yükleniyor...</div>

    <div v-else-if="contents.length > 0" class="titles-grid">
      <div
        v-for="title in contents"
        :key="title.id"
        class="small-title-card"
        :style="{ backgroundImage: `url(${title.poster || 'https://via.placeholder.com/200x300?text=No+Poster'})` }"
      >
        <button class="remove-item-btn" @click.stop="removeFromList(title.id)" title="Listeden Kaldır">
          ×
        </button>

        <div class="title-overlay">
          <div class="title-info-mini">
            <h4>{{ title.title_name }}</h4>
            <span class="year-mini">{{ title.yil }}</span>
          </div>

          <button class="mini-action-btn" @click.stop="openDetailModal(title)">Detaylar</button>
        </div>
      </div>
    </div>

    <TitleDetailModal
      :isOpen="showModal"
      :title="selectedTitle || {}"
      @close="showModal = false"
    />
  </div>
</template>

<script>
import apiClient from '@/api/axios'
import TitleDetailModal from '@/components/TitleDetailModal.vue'

export default {
  components: { TitleDetailModal },
  data() {
    return {
      listInfo: {},
      contents: [],
      loading: true,
      showModal: false,
      selectedTitle: null
    }
  },
  async mounted() {
    this.fetchListDetails();
  },
  methods: {
    async fetchListDetails() {
      const listId = this.$route.params.id;
      try {
        const response = await apiClient.get(`ozel-listeler/${listId}/`);
        this.listInfo = response.data;
        this.contents = response.data.icerikler_detay || [];
      } catch (err) {
        console.error("Hata:", err);
      } finally {
        this.loading = false;
      }
    },
    // Detayları Açma Fonksiyonu
    openDetailModal(title) {
      this.selectedTitle = title;
      this.showModal = true;
    },
    // Listeden Film Çıkarma Fonksiyonu
    async removeFromList(titleId) {
      if (!confirm("Bu içeriği listeden çıkarmak istediğinize emin misiniz?")) return;
      const listId = this.$route.params.id;
      try {
        // Backend'deki 'icerik_cikar' endpoint'ine POST atıyoruz
        await apiClient.post(`ozel-listeler/${listId}/icerik_cikar/`, { title_id: titleId });
        // Listeyi yerel olarak güncelle (sayfayı yenilemeden siler)
        this.contents = this.contents.filter(item => item.id !== titleId);
      } catch (err) {
        alert("Çıkarılırken bir hata oluştu.");
      }
    }
  }
}
</script>

<style scoped>
.list-detail-wrapper {
  padding: 40px 20px;
  background: #0f172a;
  min-height: 100vh;
  color: white;
}

.header-container { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }

/* KÜÇÜK KART TASARIMI */
.titles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); /* Kartlar küçüldü */
  gap: 15px;
}

.small-title-card {
  height: 270px; /* Boyut kısaldı */
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s;
}

.small-title-card:hover {
  transform: scale(1.03);
}

/* LİSTEDEN ÇIKAR BUTONU */
.remove-item-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 50, 50, 0.8);
  color: white;
  border: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 5;
  font-weight: bold;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-item-btn:hover { background: #ff0000; transform: scale(1.1); }

.title-overlay {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 10px;
  background: linear-gradient(transparent, rgba(0,0,0,0.9));
}

.title-info-mini h4 {
  font-size: 14px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.year-mini { font-size: 11px; opacity: 0.7; }

.mini-action-btn {
  width: 100%;
  margin-top: 8px;
  padding: 5px;
  font-size: 12px;
  background: #4cc9f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.back-btn { background: #334155; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
</style>