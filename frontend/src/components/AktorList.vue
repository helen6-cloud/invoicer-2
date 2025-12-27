<script>
import axios from "axios";

export default {
  name: "AktorList",
  data() {
    return {
      actors: [],
    };
  },
  async mounted() {
    const res = await axios.get("http://127.0.0.1:8000/api/aktorler/");
    this.actors = res.data;
  },
};
</script>

<template>
  <div>
    <h2>Oyuncular</h2>

    <ul>
      <li v-for="a in actors" :key="a.id">
        {{ a.ad }} {{ a.soyad }}
      </li>
    </ul>
  </div>
</template>
