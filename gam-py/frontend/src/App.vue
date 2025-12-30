<template>
  <div id="app">
    <AppNavbar v-if="!hideNavbar" />

    <router-view/>
  </div>
</template>

<script>
import AppNavbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    AppNavbar
  },
  computed: {
    hideNavbar() {
      const hiddenRoutes = ['login', 'cadastro']; 
      return hiddenRoutes.includes(this.$route.name);
    }
  }
}
</script>

<style>

#app {
  padding-top: var(--header-height);
}

body:has(#app > .app-header[style*="display: none"]) {
   padding-top: 0;
}
</style>