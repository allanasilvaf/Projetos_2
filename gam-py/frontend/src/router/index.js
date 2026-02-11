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
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/Calculadora',
      name: 'calculadora',
      component: () => import('../views/Calculadora.vue')
    },
    {
      path: '/Otimizador',
      name: 'Otimizador',
      component: () => import('../views/Otimizador.vue')
    },
    {
      path: '/Cadastro',
      name: 'Cadastro',
      component: () => import('../views/Cadastro.vue')
    },
    {
      path: '/ajustes', // <--- ROTA QUE ESTAMOS TESTANDO
      name: 'ajustes',
      component: () => import('../views/Ajustes.vue'),
      meta: { requiresAuth: true } // <--- TEM QUE TER ISSO AQUI
    },
    // ... suas outras rotas ...
  ]
})

// === O GUARDA DE SEGURANÇA ===
router.beforeEach((to, from, next) => {
  // Pega o usuário do navegador
  const usuarioSalvo = localStorage.getItem('user');

  console.log(`Tentando ir para: ${to.path}`);
  console.log(`Rota Protegida? ${to.meta.requiresAuth}`);
  console.log(`Tem usuário salvo? ${usuarioSalvo}`);

  // Se a rota precisa de senha (requiresAuth)
  if (to.meta.requiresAuth) {
    // Se NÃO tem usuário...
    if (!usuarioSalvo) {
      console.log("🚫 BLOQUEADO! Redirecionando para Login...");
      next('/login'); // Chuta para o login
    } else {
      console.log("✅ PERMITIDO! Usuário encontrado.");
      next(); // Deixa entrar
    }
  } else {
    // Se a rota for pública (Home, Login, Cadastro)
    next(); 
  }
});

export default router