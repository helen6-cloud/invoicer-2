<template>
  <div id="app" style="padding:20px; max-width:1100px; margin:auto;">
    <h1>Invoicer Frontend</h1>
    <nav style="margin-bottom:15px;">
      <router-link to="/invoices" style="margin-right:10px;">Invoices</router-link>
      <router-link to="/create-invoice">Create Invoice</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Basit stil */
body {
  font-family: Arial, sans-serif;
}
a {
  text-decoration: none;
  color: #007acc;
}
a.router-link-active {
  font-weight: bold;
}
</style>
