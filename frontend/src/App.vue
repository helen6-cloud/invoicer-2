<template>
  <div>
    <NavBar v-if="showNav" />
    <router-view />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  components: { NavBar },
  computed: {
    showNav() {
      return !["/login", "/register", "/forgot-password"].includes(this.$route.path);
    },
  },
};
</script>

<style>
body {
  background: #111;
  color: white;
  margin: 0;
  font-family: 'Poppins', sans-serif;
}
</style>
