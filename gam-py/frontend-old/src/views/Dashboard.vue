<template>
  <div class="dashboard">
    <h1>📊 Dashboard do GAM.py</h1>
    
    <div v-if="user" class="user-info">
      <h2>Bem-vindo, {{ user.nome }}!</h2>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Tipo:</strong> {{ user.tipo }}</p>
      <p><strong>ID:</strong> {{ user.id }}</p>
    </div>
    
    <div class="dashboard-cards">
      <div class="card">
        <h3>Calculadora CRG</h3>
        <p>Sistema funcionando com Vue.js + PHP + MySQL</p>
        <router-link to="/dashboard" class="btn-card-action">Calcular</router-link>
      </div>
      
      <div class="card">
        <h3>🔐 Autenticação</h3>
        <p>Login realizado via API REST</p>
      </div>
      
      <div class="card">
        <h3>🗄️ Banco de Dados</h3>
        <p>MySQL com tabela de usuários</p>
      </div>
    </div>
    
    <button @click="logout" class="logout-btn">
      🔓 Sair
    </button>
    
    <router-link to="/" class="back-home">
      ← Voltar para Home
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      user: null
    }
  },
  mounted() {
    // Pegar usuário do localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      this.user = JSON.parse(userData);
    } else {
      // Se não tem usuário, redirecionar para login
      this.$router.push('/login');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      this.$router.push('/login');
      alert('✅ Logout realizado!');
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 30px;
}

.user-info {
  background: #e8f5e9;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logout-btn {
  padding: 10px 20px;
  background: #ff5252;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.back-home {
  display: inline-block;
  margin-left: 20px;
  color: #42b983;
  text-decoration: none;
}
</style>