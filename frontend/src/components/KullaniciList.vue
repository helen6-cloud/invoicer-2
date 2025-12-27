<script>
import axios from "axios";

export default {
  name: "KullaniciList",
  data() {
    return {
      users: [],
    };
  },
  async mounted() {
    const res = await axios.get("http://127.0.0.1:8000/api/kullanicilar/");
    this.users = res.data;
  },
};
</script>

<template>
  <div>
    <h2>Kullanıcılar</h2>

    <ul>
      <li v-for="u in users" :key="u.id">
        {{ u.username }}
      </li>
    </ul>
  </div>
</template>
