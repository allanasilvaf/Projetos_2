<template>
  <div class="home">
    <div class="hero">
      <h1>🎓 GAM.py</h1>
      <p class="subtitle">Sistema de Gerenciamento Acadêmico para Engenharias</p>
      
      <div class="cta-buttons">
        <router-link to="/dashboard" class="cta-btn primary">
          <span class="icon">📊</span>
          <span class="text">Acessar Dashboard</span>
        </router-link>
        <router-link to="/estudantes" class="cta-btn secondary">
          <span class="icon">👨‍🎓</span>
          <span class="text">Ver Estudantes</span>
        </router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Dashboard Interativo</h3>
        <p>Acompanhe métricas em tempo real do curso de engenharia</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">👨‍🏫</div>
        <h3>Gestão de Estudantes</h3>
        <p>Controle de notas, frequência e desempenho acadêmico</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Relatórios Detalhados</h3>
        <p>Gere relatórios personalizados por disciplina ou período</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 4rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  color: #7f8c8d;
  margin-bottom: 3rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 3rem;
}

.cta-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 3rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.cta-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.cta-btn.secondary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.cta-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 4rem auto;
  padding: 0 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}
</style>
