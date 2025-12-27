<script>
import axios from "axios";

export default {
  name: "TitlesList",
  data() {
    return {
      titles: [],
      loading: true,
    };
  },
  async mounted() {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/titles/");
      this.titles = res.data;
    } catch (err) {
      console.error("Titles API error:", err);
    } finally {
      this.loading = false;
    }
  },
};
</script>

<template>
  <div>
    <h1>Film / Dizi Listesi</h1>

    <p v-if="loading">Yükleniyor...</p>

    <ul v-if="!loading">
      <li v-for="t in titles" :key="t.id">
        {{ t.baslik }} ({{ t.yil }})
      </li>
    </ul>
  </div>
</template>
