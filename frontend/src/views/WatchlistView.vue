<template>



<div class="watchlist-wrapper">

<div class="header-container">

<h1 class="page-title">📋 İzlenecekler & Listelerim</h1>

<button class="create-list-btn" @click="openCreateListModal">＋ Yeni Liste Oluştur</button>

</div>

<!-- Arama Kutusu -->

<div class="search-section">

<input

v-model="searchQuery"

type="text"

class="search-input"

placeholder="İzlenecek ara..."

@input="filterWatchlist"

/>

<span class="result-count">{{ filteredWatchlist.length }} başlık bulundu</span>

</div>

<div v-if="customLists.length > 0" class="custom-lists-container">

<div

v-for="list in customLists"

:key="list.id"

class="list-summary-card"

@click="$router.push(`/listelerim/${list.id}`)"

>

<div class="list-icon">🏵️</div>

<div class="list-details">

<span class="list-name">{{ list.isim }}</span>

<span class="list-count">{{ list.title_count || 0 }} içerik</span>

</div>

<button class="delete-list-btn" @click.stop="confirmDelete(list)">

<span class="trash-icon">🗑️</span>

</button>

</div>

</div>

<div v-if="showDeleteConfirm" class="custom-modal-overlay" @click.self="showDeleteConfirm = false">

<div class="confirm-modal-card">

<div class="confirm-icon">⚠️</div>

<h3>Listeyi Sil?</h3>

<p><strong>"{{ listToDelete?.isim }}"</strong> listesini silmek istediğinize emin misiniz? Bu işlem geri alınamaz.</p>

<div class="confirm-actions">

<button class="modal-btn cancel" @click="showDeleteConfirm = false">Vazgeç</button>

<button class="modal-btn delete-confirm" @click="handleDeleteList">Evet, Sil</button>

</div>

</div>

</div>





<!-- İzlenecekler Grid'i -->

<div v-if="loadingWatchlist" class="loading">Yükleniyor...</div>

<div v-else-if="watchlistError" class="error">{{ watchlistError }}</div>

<div v-else-if="filteredWatchlist.length > 0" class="titles-grid">

<div

v-for="item in filteredWatchlist"

:key="item.id"

class="title-card"

:style="{

backgroundImage: `url(${item.title_details.poster || 'https://via.placeholder.com/280x400?text=No+Poster'})`

}"

>

<div class="favorite-star" @click.stop="toggleFavorite(item.title_details)">

{{ favoritedTitles.has(item.title_details.id) ? '❤️' : '🤍' }}

</div>



<div class="title-overlay">

<<div class="title-header-main">

<button

v-if="!isAlreadyInList(item.title_details.id)"

class="mini-btn"

@click.stop="openAddToListModal(item.title_details)"

>

➕ Listelerime Ekle

</button>



<div v-else class="already-badge">

<span class="check-icon">✓</span> Listelerinizde Kayıtlı

</div>

</div>



<div class="title-info">

<p class="ozet">{{ item.title_details?.ozet ? item.title_details.ozet.substring(0, 80) : 'Özet yok' }}...</p>

</div>



<button class="action-btn" @click="viewDetails(item.title_details?.id)">Detaylı Gör</button>

</div>

</div>

</div>



<div v-if="showAddToListModal" class="custom-modal-overlay" @click.self="showAddToListModal = false">

<div class="custom-modal-card">

<div class="modal-header">

<h3>🎬 Listeye Ekle: {{ selectedTitleForList?.title_name }}</h3>

<button class="close-x" @click="showAddToListModal = false">×</button>

</div>

<div class="modal-body">

<div v-if="customLists.length === 0" class="no-list-warning">

<p>Henüz bir listeniz yok.</p>

<button class="create-list-btn" @click="showAddToListModal = false; openCreateListModal()">Şimdi Oluştur</button>

</div>

<div v-else class="list-selection-grid">

<button

v-for="list in customLists"

:key="list.id"

class="list-select-item"

@click="addTitleToList(list.id)"

>

📁 {{ list.isim }}

</button>

</div>

</div>

</div>

</div>



<div v-if="showCreateListModal" class="custom-modal-overlay" @click.self="closeCreateListModal">

<div class="custom-modal-card">

<div class="modal-header">

<h3>📁 Yeni Liste Oluştur</h3>

<button class="close-x" @click="closeCreateListModal">×</button>

</div>

<div class="modal-body">

<label>Liste Adı</label>

<input v-model="newListTitle" type="text" class="modal-input" @keyup.enter="handleCreateList" />

</div>

<div class="modal-footer">

<button class="modal-btn cancel" @click="closeCreateListModal">Vazgeç</button>

<button class="modal-btn confirm" :disabled="!newListTitle.trim()" @click="handleCreateList">Oluştur</button>

</div>

</div>

</div>



<TitleDetailModal

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

name: 'WatchlistView',

components: {

TitleDetailModal

},

data() {

return {

allWatchlist: [],

filteredWatchlist: [],

loadingWatchlist: false,

watchlistError: null,

searchQuery: '',

selectedTitle: null,

showModal: false,

favoritedTitles: new Set(),

showCreateListModal: false,

newListTitle: '',

customLists: [],

selectedTitleForList: null,

showAddToListModal: false,

showDeleteConfirm: false,

listToDelete: null,

}

},

async mounted() {

const token = localStorage.getItem('authToken') || localStorage.getItem('token');

if (!token) {

this.$router.push('/login');

return;

}

this.fetchCustomLists();

this.fetchWatchlist();

this.fetchFavorites();

},

methods: {



isAlreadyInList(titleId) {

if (!this.customLists) return false;

return this.customLists.some(list => {

return list.icerikler_detay && list.icerikler_detay.some(title => title.id === titleId);

});

},

async addTitleToList(listId) {

const titleId = this.selectedTitleForList?.id;

if (!titleId) {

alert("Hata: Başlık ID'si bulunamadı.");

return;

}

try {

const payload = { title_id: titleId };

await apiClient.post(`ozel-listeler/${listId}/icerik_ekle/`, payload);



this.showAddToListModal = false;



// ÖNEMLİ: Bu fonksiyon sayesinde "Ekle" butonu anında kaybolur

await this.fetchCustomLists();



// Kullanıcıya küçük bir bildirim (alert yerine daha şık olabilir)

console.log("Başarıyla eklendi ve listeler güncellendi.");

} catch (err) {

console.error("Ekleme Hatası:", err.response?.data);

alert("Eklenirken bir hata oluştu.");

}

},

viewDetails(titleId) {

// Backend yapısına göre item.title_details.id üzerinden eşleşme yapıyoruz

const item = this.allWatchlist.find(i => i.title_details.id === titleId);

if (item) {

this.selectedTitle = item.title_details;

this.showModal = true;

}

},



// 4. ARAMA FİLTRESİ: title_details içine bakacak şekilde güncelle

filterWatchlist() {

if (!this.searchQuery.trim()) {

this.filteredWatchlist = this.allWatchlist;

return;

}

const query = this.searchQuery.toLowerCase();

this.filteredWatchlist = this.allWatchlist.filter(item => {

const titleMatch = item.title_details?.title_name?.toLowerCase().includes(query);

const ozetMatch = item.title_details?.ozet?.toLowerCase().includes(query);

return titleMatch || ozetMatch;

});

},



// 5. LİSTE SİLME (MODAL İLE):

confirmDelete(list) {

this.listToDelete = list;

this.showDeleteConfirm = true;

},



async handleDeleteList() {

if (!this.listToDelete) return;

try {

await apiClient.delete(`ozel-listeler/${this.listToDelete.id}/`);

this.customLists = this.customLists.filter(l => l.id !== this.listToDelete.id);

this.showDeleteConfirm = false;

this.listToDelete = null;

} catch (err) {

alert("Liste silinirken bir hata oluştu.");

}

},



leInAnyList(titleId) {

return this.customLists.some(list =>

list.icerikler_detay && list.icerikler_detay.some(item => item.id === titleId)

);

},



async deleteCustomList(listId) {

if (!confirm("Bu listeyi ve içindeki tüm kayıtları silmek istediğinize emin misiniz?")) return;



try {

await apiClient.delete(`ozel-listeler/${listId}/`);



this.customLists = this.customLists.filter(l => l.id !== listId);

alert("Liste başarıyla silindi.");

} catch (err) {

console.error("Silme hatası:", err);

alert("Liste silinirken bir hata oluştu.");

}

},

async fetchWatchlist() {

try {

this.loadingWatchlist = true

this.watchlistError = null

const token = localStorage.getItem('authToken') || localStorage.getItem('token')



if (!token) {

this.watchlistError = 'Lütfen giriş yapınız'

return

}

const response = await apiClient.get('izlenecekler/')



this.allWatchlist = response.data.sort((a, b) => new Date(b.eklenme_tarihi) - new Date(a.eklenme_tarihi))

this.filteredWatchlist = this.allWatchlist

} catch (err) {

console.error('Fetch watchlist error:', err)

this.watchlistError = 'İzlenecekler yüklenemedi'

} finally {

this.loadingWatchlist = false

}

},

async fetchFavorites() {

try {

const token = localStorage.getItem('authToken') || localStorage.getItem('token')

if (!token) return

const response = await apiClient.get('favoriler/')

this.favoritedTitles = new Set(response.data.map(fav => fav.title))

} catch (err) {

console.error('Fetch favorites error:', err)

}

},

async fetchCustomLists() {

try {

const response = await apiClient.get('ozel-listeler/');

this.customLists = response.data;

} catch (err) { console.error(err); }

},



closeModal() { this.showModal = false; this.selectedTitle = null; },

openCreateListModal() { this.showCreateListModal = true; this.newListTitle = ''; },

closeCreateListModal() { this.showCreateListModal = false; },

openAddToListModal(titleObj) {

console.log("Modala Gelen Veri:", titleObj); // <--- Bunu ekle, F12 konsolunda ID var mı bak



if (!titleObj || !titleObj.id) {

console.error("Hata: Gelen nesne boş veya ID içermiyor!", titleObj);

return;

}



this.selectedTitleForList = titleObj;

this.showAddToListModal = true;

},



async handleCreateList() {

if (!this.newListTitle.trim()) return;

try {

await apiClient.post('ozel-listeler/', { isim: this.newListTitle });

this.closeCreateListModal();

this.fetchCustomLists();

} catch (err) {

alert("Liste oluşturulamadı.");

}

},

async toggleFavorite(title) {

try {

const token = localStorage.getItem('authToken') || localStorage.getItem('token')

if (!token) {

alert('Favorilere eklemek için giriş yapmanız gereklidir')

return

}

const response = await apiClient.get('favoriler/')

const favId = response.data.find(fav => fav.title === title.id)?.id



if (favId) {

await apiClient.delete(`favoriler/${favId}/`)

this.favoritedTitles.delete(title.id)

alert('Favorilerden kaldırıldı')

} else {

await apiClient.post('favoriler/', {title: title.id})

this.favoritedTitles.add(title.id)

alert('Favorilere eklendi!')

}

} catch (err) {

console.error('Favorite error:', err)

alert('Hata: ' + (err.response?.data?.detail || err.message))

}

},



async removeFromWatchlist(id) {

if (!confirm("Bu içeriği listenizden çıkarmak istediğinize emin misiniz?")) return;

try {

await apiClient.delete(`izlenecekler/${id}/`);

this.allWatchlist = this.allWatchlist.filter(item => item.id !== id);

this.filterWatchlist();

alert("Listeden kaldırıldı.");

} catch (err) {

console.error("Silme hatası:", err);

alert("Silerken bir hata oluştu.");

}

}

}

}



</script>



<style scoped>

.watchlist-wrapper {

width: 100%;

min-height: 100vh;

background: linear-gradient(135deg, #4c6ef5, #7950f2, #d6336c);

background-size: 300% 300%;

animation: gradientShift 12s ease infinite;

padding: 60px 20px;

color: white;

}



.page-title {

font-size: 42px;

font-weight: bold;

text-align: center;

margin-bottom: 40px;

animation: fadeIn 1s ease forwards;

}



.search-section {

max-width: 1200px;

margin: 0 auto 50px;

display: flex;

gap: 15px;

align-items: center;

justify-content: center;

}



.search-input {

flex: 1;

max-width: 500px;

padding: 12px 20px;

border: none;

border-radius: 25px;

background: rgba(255, 255, 255, 0.2);

color: white;

font-size: 16px;

backdrop-filter: blur(10px);

transition: all 0.3s ease;

}



.search-input::placeholder {

color: rgba(255, 255, 255, 0.6);

}



.search-input:focus {

outline: none;

background: rgba(255, 255, 255, 0.3);

box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);

}



.result-count {

background: rgba(255, 255, 255, 0.2);

padding: 10px 20px;

border-radius: 20px;

font-size: 14px;

backdrop-filter: blur(10px);

}



.titles-grid {

display: grid;

grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));

gap: 20px;

padding: 0 20px;

max-width: 1200px;

margin: 0 auto;

}



.title-card {

background: rgba(255, 255, 255, 0.1);

border-radius: 12px;

backdrop-filter: blur(5px);

transition: all 0.3s ease;

border: 1px solid rgba(255, 255, 255, 0.2);

background-size: cover;

background-position: center;

position: relative;

min-height: 400px;

overflow: hidden;

}



.title-card::before {

content: '';

position: absolute;

top: 0;

left: 0;

right: 0;

bottom: 0;

background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.9));

z-index: 1;

}



.favorite-star {

position: absolute;

top: 15px;

right: 15px;

background: rgba(255, 100, 150, 0.8);

width: 40px;

height: 40px;

border-radius: 50%;

display: flex;

align-items: center;

justify-content: center;

font-size: 20px;

cursor: pointer;

transition: all 0.2s ease;

z-index: 3;

border: none;

padding: 0;

}



.favorite-star:hover {

background: rgba(255, 100, 150, 1);

transform: scale(1.15);

box-shadow: 0 0 15px rgba(255, 100, 150, 0.6);

}



.title-overlay {

position: relative;

z-index: 2;

height: 100%;

display: flex;

flex-direction: column;

justify-content: space-between;

padding: 15px;

background: linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0.4) 50%, transparent 100%);

}



.title-card:hover {

transform: translateY(-5px);

box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);

}



.title-header {

display: flex;

justify-content: space-between;

align-items: start;

margin-bottom: 10px;

}



.title-header h4 {

margin: 0;

flex: 1;

font-size: 18px;

text-align: left;

color: white;

}



.year {

background: rgba(255, 255, 255, 0.3);

padding: 4px 10px;

border-radius: 6px;

font-size: 12px;

white-space: nowrap;

margin-left: 10px;

color: white;

}



.title-info {

text-align: left;

margin-bottom: 15px;

margin-top: auto;

}



.title-info p {

margin: 8px 0;

font-size: 13px;

opacity: 0.95;

line-height: 1.4;

color: white;

}



.ozet {

color: #ddd;

}



.duration {

font-size: 12px;

}



.type {

display: inline-block;

background: rgba(255, 204, 0, 0.3);

color: #ffff00;

padding: 4px 10px;

border-radius: 4px;

font-size: 12px;

font-weight: bold;

}



.action-btn {

width: 100%;

padding: 10px;

background: linear-gradient(135deg, #ffcc00, #ffaa00);

color: #333;

border: none;

border-radius: 8px;

font-weight: bold;

cursor: pointer;

transition: all 0.3s ease;

font-size: 14px;

}



.action-btn:hover {

transform: scale(1.05);

box-shadow: 0 4px 12px rgba(255, 204, 0, 0.4);

}



.loading {

text-align: center;

padding: 60px 20px;

font-size: 18px;

opacity: 0.8;

}



.error {

text-align: center;

padding: 20px;

background: rgba(255, 100, 100, 0.2);

border: 2px solid rgba(255, 100, 100, 0.5);

border-radius: 8px;

color: #ffcccc;

margin: 0 20px;

}



.no-results {

text-align: center;

padding: 60px 20px;

font-size: 24px;

color: rgba(255, 255, 255, 0.6);

}



@keyframes fadeIn {

from { opacity: 0; transform: translateY(10px); }

to { opacity: 1; transform: translateY(0); }

}



@keyframes gradientShift {

0% { background-position: 0% 50%; }

50% { background-position: 100% 50%; }

100% { background-position: 0% 50%; }

}



@media (max-width: 768px) {

.page-title {

font-size: 32px;

}

.titles-grid {

grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));

gap: 15px;

}



.search-section {

flex-direction: column;

}

.search-input {

max-width: none;

}

}

.header-container {

display: flex;

justify-content: space-between;

align-items: center;

max-width: 1200px;

margin: 0 auto 30px;

}



.create-list-btn {

background: #40c057;

color: white;

border: none;

padding: 10px 20px;

border-radius: 8px;

font-weight: bold;

cursor: pointer;

transition: 0.3s;

}



.create-list-btn:hover {

background: #37b24d;

transform: scale(1.05);

}



.remove-btn {

position: absolute;

top: 12px;

left: 12px;

background: rgba(255, 0, 0, 0.7);

width: 35px;

height: 35px;

border-radius: 50%;

display: flex;

align-items: center;

justify-content: center;

cursor: pointer;

z-index: 3;

transition: 0.2s;

}



.remove-btn:hover {

background: rgba(255, 0, 0, 1);

transform: scale(1.1);

}

.custom-modal-overlay {

position: fixed;

top: 0;

left: 0;

width: 100%;

height: 100%;

background: rgba(0, 0, 0, 0.8);

backdrop-filter: blur(8px);

display: flex;

align-items: center;

justify-content: center;

z-index: 1000;

animation: fadeIn 0.3s ease;

}



/* Modal Kartı */

.custom-modal-card {

background: #1e1e1e;

width: 90%;

max-width: 450px;

border-radius: 16px;

border: 1px solid rgba(255, 255, 255, 0.1);

box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);

overflow: hidden;

animation: slideUp 0.3s ease;

}



.modal-header {

padding: 20px;

background: rgba(255, 255, 255, 0.05);

display: flex;

justify-content: space-between;

align-items: center;

}



.modal-header h3 {

margin: 0;

font-size: 20px;

color: #fff;

}



.close-x {

background: none;

border: none;

color: #aaa;

font-size: 28px;

cursor: pointer;

}



.modal-body {

padding: 30px 20px;

}



.modal-body label {

display: block;

margin-bottom: 10px;

color: #ccc;

font-size: 14px;

}



.modal-input {

width: 100%;

padding: 12px 15px;

background: rgba(255, 255, 255, 0.1);

border: 1px solid rgba(255, 255, 255, 0.2);

border-radius: 8px;

color: white;

font-size: 16px;

transition: 0.3s;

}



.modal-input:focus {

outline: none;

border-color: #40c057;

background: rgba(255, 255, 255, 0.15);

}



.modal-body small {

display: block;

margin-top: 10px;

color: #666;

}



.modal-footer {

padding: 20px;

display: flex;

gap: 12px;

justify-content: flex-end;

background: rgba(0, 0, 0, 0.2);

}



.modal-btn {

padding: 10px 20px;

border-radius: 8px;

border: none;

font-weight: bold;

cursor: pointer;

transition: 0.2s;

}



.modal-btn.cancel {

background: rgba(255, 255, 255, 0.1);

color: #fff;

}



.modal-btn.confirm {

background: #40c057;

color: white;

}



.modal-btn.confirm:disabled {

background: #2b5e36;

opacity: 0.5;

cursor: not-allowed;

}



.modal-btn:hover:not(:disabled) {

transform: translateY(-2px);

}



@keyframes slideUp {

from { transform: translateY(30px); opacity: 0; }

to { transform: translateY(0); opacity: 1; }

}

/* Özel Liste Kartları Bölümü */

.custom-lists-container {

display: flex;

gap: 15px;

overflow-x: auto;

padding: 10px 0 30px;

max-width: 1200px;

margin: 0 auto;

scrollbar-width: thin;

}



.list-summary-card {

min-width: 180px;

background: rgba(255, 255, 255, 0.1);

backdrop-filter: blur(10px);

padding: 15px;

border-radius: 12px;

display: flex;

align-items: center;

gap: 12px;

border: 1px solid rgba(255, 255, 255, 0.1);

cursor: pointer;

transition: 0.3s;

}



.list-summary-card:hover {

background: rgba(255, 255, 255, 0.2);

transform: translateY(-3px);

}



.list-icon { font-size: 24px; }



.list-name {

display: block;

font-weight: bold;

font-size: 14px;

}



.list-count {

font-size: 12px;

color: #ccc;

}



.mini-btn {

background: rgba(0, 0, 0, 0.6);

color: white;

border: 1px solid rgba(255, 255, 255, 0.3);

padding: 6px 12px;

border-radius: 6px;

font-size: 11px;

cursor: pointer;

margin-bottom: 5px;

}



.mini-btn:hover {

background: white;

color: black;

}

.list-selection-grid {

display: flex;

flex-direction: column;

gap: 10px;

max-height: 300px;

overflow-y: auto;

}



.list-select-item {

background: rgba(255, 255, 255, 0.05);

border: 1px solid rgba(255, 255, 255, 0.1);

color: white;

padding: 12px;

border-radius: 8px;

text-align: left;

cursor: pointer;

transition: 0.2s;

}



.list-select-item:hover {

background: #40c057;

transform: translateX(5px);

}



.no-list-warning {

text-align: center;

color: #aaa;

}

.list-summary-card-wrapper {

position: relative;

display: flex;

align-items: center;

}



.delete-list-btn {

position: absolute;

top: -5px;

right: -5px;

background: #ff4d4f;

border: none;

border-radius: 50%;

width: 24px;

height: 24px;

cursor: pointer;

display: flex;

align-items: center;

justify-content: center;

font-size: 12px;

transition: 0.3s;

z-index: 10;

box-shadow: 0 2px 5px rgba(0,0,0,0.2);

}



.delete-list-btn:hover {

transform: scale(1.2);

background: #ff7875;

}



.already-in-list {

font-size: 11px;

color: #40c057;

font-weight: bold;

background: rgba(64, 192, 87, 0.1);

padding: 4px 8px;

border-radius: 4px;

}

/* Liste Kutucuğu Wrapper */

.list-summary-card-wrapper {

position: relative;

display: flex;

align-items: center;

}



/* Çöp Kutusu Butonu */

.delete-list-btn {

position: absolute;

top: -8px;

right: -8px;

background: #ff4d4f;

border: none;

width: 28px;

height: 28px;

border-radius: 50%;

display: flex;

align-items: center;

justify-content: center;

cursor: pointer;

box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);

transition: all 0.2s ease;

z-index: 5;

}



.delete-list-btn:hover {

transform: scale(1.15) rotate(10deg);

background: #ff7875;

}



.trash-icon { font-size: 14px; }



/* Onay Modalı Kartı */

.confirm-modal-card {

background: #1e1e2e;

width: 90%;

max-width: 350px;

padding: 30px;

border-radius: 20px;

text-align: center;

border: 1px solid rgba(255, 255, 255, 0.1);

box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);

animation: modalPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);

}



.confirm-icon {

font-size: 50px;

margin-bottom: 15px;

}



.confirm-modal-card h3 {

margin: 0 0 10px;

color: white;

font-size: 22px;

}



.confirm-modal-card p {

color: #a0a0ba;

font-size: 14px;

line-height: 1.5;

margin-bottom: 25px;

}



.confirm-actions {

display: flex;

gap: 12px;

justify-content: center;

}



/* Silme Butonu Özel Rengi */

.modal-btn.delete-confirm {

background: #ff4d4f;

color: white;

}



.modal-btn.delete-confirm:hover {

background: #ff7875;

box-shadow: 0 0 15px rgba(255, 77, 79, 0.4);

}



/* Animasyon */

@keyframes modalPop {

from { opacity: 0; transform: scale(0.8); }

to { opacity: 1; transform: scale(1); }

}

.already-badge {

display: flex;

align-items: center;

gap: 5px;

background: rgba(64, 192, 87, 0.15);

color: #40c057;

padding: 6px 12px;

border-radius: 20px;

font-size: 12px;

font-weight: 600;

border: 1px solid rgba(64, 192, 87, 0.3);

animation: fadeIn 0.3s ease;

}



.check-icon {

font-weight: bold;

}



@keyframes fadeIn {

from { opacity: 0; transform: translateY(5px); }

to { opacity: 1; transform: translateY(0); }

}



.already-badge {

display: flex;

align-items: center;

gap: 5px;

background: rgba(64, 192, 87, 0.2);

color: #40c057;

padding: 6px 12px;

border-radius: 20px;

font-size: 11px;

font-weight: bold;

border: 1px solid rgba(64, 192, 87, 0.4);

box-shadow: 0 0 10px rgba(64, 192, 87, 0.2);

animation: badgeAppear 0.5s ease-out;

}



@keyframes badgeAppear {

0% { transform: scale(0.8); opacity: 0; }

50% { transform: scale(1.1); }

100% { transform: scale(1); opacity: 1; }

}

</style>