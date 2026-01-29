<template>
  <header class="fixed top-0 left-0 w-full h-[80px] z-50 shadow-md bg-primary text-white">
    
    <div class="h-full max-w-7xl mx-auto px-5 flex justify-between items-center">
      
      <div class="flex items-center gap-2">
        <img src="@/assets/logo-verde.svg" alt="Logo GAM.py" class="h-10 w-auto">
      </div>

      <nav class="hidden md:flex gap-8">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <Home :size="20" class="nav-icon" />
          Início
        </router-link>
        
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <LayoutDashboard :size="20" class="nav-icon" />
          Painel
        </router-link>
        
        <router-link to="/ajustes" class="nav-item" active-class="active">
          <Settings :size="20" class="nav-icon" />
          Ajustes
        </router-link>
      </nav>

      <div class="flex items-center gap-4">
        <router-link to="/login" class="btn-action">
          Acessar Portal
        </router-link>
        
        <div class="profile-icon">
          <User :size="20" />
        </div>
      </div>

    </div>
  </header>
</template>

<script>
import { 
  Home, 
  LayoutDashboard, 
  Users, 
  Settings, 
  User 
} from 'lucide-vue-next';

export default {
  name: 'AppNavbar',
  components: {
    Home,
    LayoutDashboard,
    Users,
    Settings,
    User
  }
}
</script>

<style scoped>

.nav-item {
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 6px 0;
  border-bottom: 2px solid transparent; /* Prepara para o sublinhado */
}

/* Efeito Hover e Ativo */
.nav-item:hover, .nav-item.active {
  color: white;
  transform: translateY(-1px);
}

.nav-item.active {
  font-weight: 600;
  border-bottom: 2px solid white; /* Sublinhado branco quando ativo */
}

/* Botão Acessar Portal */
.btn-action {
  background: rgba(255, 255, 255, 0.2); /* Fundo de vidro */
  color: white;
  padding: 8px 18px;
  border-radius: 9999px; /* Pill shape */
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
  text-decoration: none;
  border: 1px solid rgba(255,255,255,0.3);
}

.btn-action:hover {
  background: white;
  color: var(--color-primary, #6BA368); /* Texto fica verde no hover */
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Ícone de Perfil */
.profile-icon {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary, #6BA368); /* Ícone verde */
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-icon:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}
</style>