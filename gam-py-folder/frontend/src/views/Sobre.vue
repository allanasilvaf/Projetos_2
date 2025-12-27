<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>
<template>
  <div class="about">
    <div class="about-container">
      <div class="about-header">
        <h1>🎓 Sobre o GAM.py</h1>
        <p class="subtitle">Gerenciador Acadêmico para Engenharias</p>
      </div>

      <div class="about-content">
        <section class="mission-section">
          <div class="section-icon">🎯</div>
          <h2>Missão</h2>
          <p>
            O GAM.py tem como objetivo facilitar a gestão acadêmica de cursos 
            de engenharia, fornecendo ferramentas intuitivas para coordenadores 
            acompanharem o desempenho dos estudantes e tomarem decisões 
            baseadas em dados.
          </p>
        </section>

        <section class="features-section">
          <h2>✨ Funcionalidades Principais</h2>
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">📊</div>
              <h3>Dashboard Interativo</h3>
              <p>Visualize métricas em tempo real com gráficos e indicadores</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">👨‍🎓</div>
              <h3>Gestão de Estudantes</h3>
              <p>Controle completo de dados, notas, frequência e histórico</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">📈</div>
              <h3>Relatórios Avançados</h3>
              <p>Gere relatórios personalizados por curso, disciplina ou período</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🔔</div>
              <h3>Sistema de Alertas</h3>
              <p>Notificações automáticas para estudantes em situação de risco</p>
            </div>
          </div>
        </section>

        <section class="target-section">
          <h2>👥 Público-Alvo</h2>
          <div class="target-grid">
            <div class="target-card">
              <h3>Coordenadores</h3>
              <p>Tenha uma visão macro do curso e tome decisões estratégicas</p>
            </div>
            <div class="target-card">
              <h3>Professores</h3>
              <p>Acompanhe o desempenho individual de cada estudante</p>
            </div>
            <div class="target-card">
              <h3>Estudantes</h3>
              <p>Monitore seu próprio progresso acadêmico</p>
            </div>
          </div>
        </section>

        <section class="tech-section">
          <h2>🛠️ Tecnologias Utilizadas</h2>
          <div class="tech-stack">
            <div class="tech-item">
              <div class="tech-logo">⚡</div>
              <h4>Vue.js 2</h4>
              <p>Framework JavaScript progressivo para interface</p>
            </div>
            <div class="tech-item">
              <div class="tech-logo">🎨</div>
              <h4>CSS3 & SCSS</h4>
              <p>Estilização moderna e responsiva</p>
            </div>
            <div class="tech-item">
              <div class="tech-logo">🔄</div>
              <h4>Vue Router</h4>
              <p>Navegação entre páginas sem recarregar</p>
            </div>
            <div class="tech-item">
              <div class="tech-logo">📊</div>
              <h4>Chart.js</h4>
              <p>Visualização de dados em gráficos</p>
            </div>
          </div>
        </section>

        <section class="contact-section">
          <h2>📞 Contato</h2>
          <p>
            Para mais informações, sugestões ou suporte técnico, 
            entre em contato através do email:
          </p>
          <div class="contact-info">
            <p><strong>Email:</strong> suporte@gam-py.edu.br</p>
            <p><strong>Desenvolvedora:</strong> Allana Silva</p>
            <p><strong>Projeto:</strong> Sistema Acadêmico GAM.py</p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      version: '1.0.0',
      lastUpdate: 'Dezembro 2024'
    }
  }
}
</script>

<style scoped>
.about {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 2rem;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  overflow: hidden;
}

.about-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.about-header h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  opacity: 0.9;
}

.about-content {
  padding: 3rem 2rem;
}

section {
  margin-bottom: 4rem;
}

h2 {
  color: #2c3e50;
  font-size: 2.2rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 3px solid #f0f0f0;
}

.mission-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 4rem;
}

.section-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.mission-section p {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #555;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2.5rem;
  margin-top: 2rem;
}

.feature-item {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #e9ecef;
}

.feature-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature-item h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.4rem;
}

.target-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.target-card {
  background: linear-gradient(135deg, #f0f4ff 0%, #e6f7ff 100%);
  padding: 2.5rem;
  border-radius: 15px;
  text-align: center;
  border-left: 5px solid #667eea;
}

.target-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.tech-item {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.tech-logo {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.tech-item h4 {
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
}

.contact-section {
  background: #f0f7ff;
  padding: 3rem;
  border-radius: 15px;
  margin-top: 3rem;
}

.contact-info {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  margin-top: 1.5rem;
  max-width: 600px;
}

.contact-info p {
  margin: 0.75rem 0;
  font-size: 1.1rem;
  color: #555;
}

@media (max-width: 768px) {
  .about-header h1 {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  h2 {
    font-size: 1.8rem;
  }
  
  .about-content {
    padding: 2rem 1rem;
  }
}
</style>