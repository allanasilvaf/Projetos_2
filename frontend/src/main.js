import Vue from 'vue'
import App from './App.vue'
import router from './router'  // ← IMPORTANTE: importar o router

Vue.config.productionTip = false

new Vue({
  router,  // ← IMPORTANTE: passar o router aqui
  render: h => h(App)
}).$mount('#app')