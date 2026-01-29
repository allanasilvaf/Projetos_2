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

<style>

::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f4f6f8;
}

::-webkit-scrollbar-thumb {
  background-color: #a5c9a3; 
  border-radius: 10px;       

  border: 2px solid #f4f6f8; 
}

::-webkit-scrollbar-thumb:hover {
  background-color: #6BA368; 
}

html {
  scrollbar-width: thin;          
  scrollbar-color: #6BA368 #f4f6f8;
}
</style>