<template>
  <div class="movie-list">
    <h2>🎬 Film Listesi</h2>
    <div v-if="loading">Yükleniyor...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <ul v-if="movies.length">
      <li v-for="icerik in movies" :key="movie.id">
        <strong>{{ icerik.title }}</strong>
        ({{movie.genre}})
        ⭐ {{ movie.rating }}
      </li>
    </ul>

  </div>
</template>

<script>
import apiClient from "@/api/axios";


export default {
  name: "MovieList",

  data(){
    return{
      movies: [],
      loading: false,
      error:"",
   };
  },

  mounted() {
    this.getMovies();
  },
  methods: {
    async getMovies() {
      this.loading = true;
      this.error = "";

      try {
        const response = await apiClient.get("/icerik/");
        this.movies = response.data;
      } catch (err) {
        console.error("API Hata Detayı:", err);
        this.error = "Filmler yüklenirken bir hata oluştu.";
      }
      finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.error {
  color: red;
  margin-top: 10px;
}
</style>