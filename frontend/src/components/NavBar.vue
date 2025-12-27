<template>
  <nav class="navbar animate-slide">
    <div class="logo" @click="go('/')">🎬 Film&Dizi</div>


    <div class="search-container">
      <input
        v-model="searchQuery"
        type="text"
        class="search-input"
        placeholder="Film, dizi ara..."
        @input="handleSearchInput"
        @keyup.enter="handleSearch"
      />
      <button class="search-btn" @click="handleSearch">🔍</button>
    </div>

    <ul class="menu">
      <li @click="go('/')">Ana Sayfa</li>
      <li @click="go('/filmler')">🎬 Filmler</li>
      <li @click="go('/diziler')">📺 Diziler</li>
      <li @click="go('/onerilenler')">✨ Önerilenler</li>
      <li @click="go('/favoriler')"> ❤️ Favoriler</li>
      <li @click="go('/izlenecekler')">📋 İzlenecekler</li>
    </ul>

    <button class="logout" @click="logout">Çıkış</button>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    go(path) {
      this.$router.push(path)
    },
    handleSearchInput() {

      if (this.searchQuery.trim().length > 0) {
        this.$emit('update-search', this.searchQuery)
      }
    },
    handleSearch() {
      if (this.searchQuery.trim()) {

        this.$router.push({
          name: 'Home',
          query: { search: this.searchQuery }
        })
      }
    },
    logout() {
      localStorage.removeItem("authToken")
      localStorage.removeItem("token")
      this.$router.push("/login")
    }
  }
}
</script>

<style scoped>
.navbar {
  width: 100%;
  padding: 14px 32px;
  display: flex;
  align-items: center;
  gap: 24px;

  background: linear-gradient(135deg, #141414, #1f1f1f);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(10px);

  box-sizing: border-box;
}
.logo {
  font-size: 26px;
  font-weight: bold;
  cursor: pointer;

}

.menu {
  display: flex;
  gap: 25px;
  list-style: none;
  justify-content: center;
}


.search-container {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 25px;
  padding: 8px 15px;
  margin: 0 30px;
  gap: 10px;
  min-width: 250px;
}

.search-input {
  background: transparent;
  border: none;
  color: white;
  font-size: 14px;
  outline: none;
  width: 100%;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.search-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: 0.2s;
  padding: 0;
}

.search-btn:hover {
  transform: scale(1.2);
  color: #ffdd55;
}

.logout {
  background: linear-gradient(135deg, #ff4d4d, #ff1f1f);
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  color: white;
  white-space: nowrap;
  flex-shrink: 0;

  transition: all 0.25s ease;
}

.logout:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(255,77,77,0.6);
}

/* ===== ANIMATION ===== */
.animate-slide {
  animation: slideDown 0.6s ease forwards;
}

@keyframes slideDown {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 1024px) {
  .menu {
    display: none; /* mobilde gizle */
  }

  .search-container {
    flex: 1;
    max-width: none;
  }
}
</style>
