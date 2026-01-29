<template>
  <header class="app-header">
    <div class="header-container">
      
      <div class="header-left">
        <img src="@/assets/logo-verde.svg" alt="Logo GAM.py" class="header-logo">
      </div>

      <nav class="header-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <home-icon size="1.2x" class="nav-icon"></home-icon>
          Início
        </router-link>
        
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <layout-icon size="1.2x" class="nav-icon"></layout-icon>
          Painel
        </router-link>
        
        <!-- <router-link to="/alunos" class="nav-item" active-class="active">
          <users-icon size="1.2x" class="nav-icon"></users-icon>
          Alunos
        </router-link> -->
        
        <router-link to="/ajustes" class="nav-item" active-class="active">
          <settings-icon size="1.2x" class="nav-icon"></settings-icon>
          Ajustes
        </router-link>
      </nav>

      <div class="header-right">
        <router-link to="/login" class="btn-action">Acessar Portal</router-link>
        <div class="profile-icon">
          <user-icon size="1.2x" class="nav-icon"></user-icon>
        </div>
      </div>

    </div>
  </header>
</template>

<script>

import { 
  HomeIcon, 
  LayoutIcon, 
  UsersIcon, 
  SettingsIcon, 
  UserIcon 
} from 'vue-feather-icons';

export default {
  name: 'AppNavbar',
  // 2. Registro dos componentes
  components: {
    HomeIcon,
    LayoutIcon,
    UsersIcon,
    SettingsIcon,
    UserIcon
  }
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--header-height);
  background-color: var(--color-bg-header);
  color: var(--color-text-light);
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: var(--container-width);
  margin: 0 auto;
  height: 100%;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-logo {
  height: 40px; 
  width: auto;
}

.header-nav {
  display: flex;
  gap: 25px;
}

.nav-item {
  color: rgba(255,255,255, 0.8);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  text-decoration: none;
  font-size: 0.95rem;
}

.nav-icon {
  stroke-width: 2;
  transition: transform 0.2s;
}

.nav-item:hover, .nav-item.active {
  color: white;
  text-decoration: none;
}

.nav-item:hover .nav-icon {
  transform: translateY(-2px);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn-action {
  background: rgba(255,255,255,0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  transition: background 0.2s;
  text-decoration: none;
  font-size: 0.9rem;
}

.btn-action:hover {
  background: white;
  color: var(--color-primary);
}

.profile-icon {
  width: 38px;
  height: 38px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  cursor: pointer;
  transition: transform 0.2s;
}

.profile-icon:hover {
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .header-nav { display: none; }
}
</style>