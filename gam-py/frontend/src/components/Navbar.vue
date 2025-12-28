<template>
  <header class="app-header">
    <div class="header-container">
      
      <div class="header-left">
        <img src="@/assets/logo.png" alt="Logo GAM.py" class="header-logo">
        <span class="logo-text">GAM.py</span>
      </div>

      <nav class="header-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <span class="icon">🏠</span> Início
        </router-link>
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <span class="icon">📊</span> Painel
        </router-link>
        <router-link to="/alunos" class="nav-item" active-class="active">
          <span class="icon">👥</span> Alunos
        </router-link>
        <router-link to="/ajustes" class="nav-item" active-class="active">
          <span class="icon">⚙️</span> Ajustes
        </router-link>
      </nav>

      <div class="header-right">
        <router-link to="/login" class="btn-action">Acessar Portal</router-link>
        <div class="profile-icon">👤</div>
      </div>

    </div>
  </header>
</template>

<script>
export default {
  name: 'AppNavbar'
}
</script>

<style scoped>
/* Aqui trazemos apenas o CSS que é EXCLUSIVO da Navbar.
  Usamos as variáveis globais do main.css para manter a consistência.
*/

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

.logo-text {
  font-weight: 700;
  font-size: 1.2rem;
  color: white;
}

.header-nav {
  display: flex;
  gap: 25px;
  /* Esconde o menu em telas muito pequenas */
  @media (max-width: 768px) {
    display: none;
  }
}

.nav-item {
  color: rgba(255,255,255, 0.9);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s;
  text-decoration: none;
}

.nav-item:hover, .nav-item.active {
  color: white;
  text-decoration: underline;
  text-underline-offset: 4px;
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
  width: 35px;
  height: 35px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  cursor: pointer;
}
</style>