// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('../views/Cadastro.vue')
    },
    {
      path: '/ajustes',
      name: 'ajustes',
      component: () => import('../views/Ajustes.vue')
    },
    {
      path: '/Forgotpassword',
      name: 'Forgotpassword',
      component: () => import('../views/Forgotpassword.vue')
    },
    {
      path: '/Calculadora',
      name: 'Calculadora',
      component: () => import('../views/Calculadora.vue')
    },
    {
      path: '/Otimizador',
      name: 'Otimizador',
      component: () => import('../views/Otimizador.vue')
    }
    
  ]

})

export default router