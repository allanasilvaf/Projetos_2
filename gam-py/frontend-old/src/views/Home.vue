<template>
  <div class="home-content-wrapper">

    <div class="first-fold">
      <section class="hero-section">
        <div class="hero-content">
          <div class="hero-badge-title">
            <h1>Assuma o controle da sua graduação!</h1>
          </div>
          <p class="hero-subtitle">
            Acompanhe seu CRG em tempo real, gerencie faltas e planeje o semestre ideal em um único lugar.
          </p>
        </div>
      </section>

      <main class="main-grid-section">
        <div class="grid-container">
          
          <div class="grid-col-left stacked-images">
            <img src="@/assets/img-1.png" class="grid-image img-half-height">
            <img src="@/assets/img-2.png" class="grid-image img-half-height">
          </div>

          <div class="grid-col-center">
            <img src="@/assets/img-3.png" class="grid-image img-full-height">
          </div>

          <div class="grid-col-right">
            <img src="@/assets/img-4.png" class="grid-image img-full-height">
          </div>

        </div>
      </main>

      <div class="scroll-indicator-container">
        <button class="scroll-btn" @click="scrollToFeatures">⬇</button>
      </div>
    </div>

    <section id="funcionalidades" class="features-section">
      
      <div class="badge-container">
        <span class="pill-badge">Recursos Exclusivos</span>
      </div>

      <div class="features-header">
        <h2>Inteligência de Dados Aplicada à sua Graduação</h2>
        <p>Utilize métricas precisas para prever seu desempenho, otimizar sua grade horária e garantir sua formação no tempo certo.</p>
      </div>

      <div class="cards-grid">
        
        <div class="feature-card">
          <div class="card-text-area">
            <h3>Calculadora de CRG</h3>
            <p>Simule seu Coeficiente de Rendimento Geral (CRG) final com base na sua frequência atual e notas parciais.</p>
            <router-link to="/dashboard" class="btn-card-action">Simular Agora</router-link>
          </div>
          <div class="card-visual-area">
            <img src="https://img.freepik.com/fotos-gratis/close-up-da-mao-usando-uma-calculadora_1220-58.jpg?t=st=1767124314~exp=1767127914~hmac=b6dd182c0256705507cf16c05f9aa87ded005f6f5954e5cef8ca81b971051eb2&w=1480" alt="Notas">
          </div>
        </div>

        <div class="feature-card">
          <div class="card-text-area">
            <h3>Otimizador de Semestre</h3>
            <p>Receba recomendações inteligentes das melhores disciplinas e optativas para cursar.</p>
            <router-link to="/dashboard" class="btn-card-action">Montar Grade</router-link>
          </div>
          <div class="card-visual-area">
            <img src="https://img.freepik.com/fotos-gratis/jigsaw-trabalho-em-equipe-conceito-tiro-macro_53876-17929.jpg?t=st=1767124501~exp=1767128101~hmac=295dee323fe380307e6df1e3a1fbeaa991891c0725e824dc3254dd5103d358d2&w=1060" alt="Frequência">
          </div>
        </div>

        <div class="feature-card">
          <div class="card-text-area">
            <h3>Análise de Desempenho</h3>
            <p>Visualize seu progresso com gráficos detalhados e identifique quais matérias exigem mais atenção.</p>
            <router-link to="/dashboard" class="btn-card-action">Ver Relatório</router-link>
          </div>
          <div class="card-visual-area">
            <img src="https://img.freepik.com/fotos-gratis/alto-angulo-de-dardo-na-mosca_23-2148443764.jpg?t=st=1767124569~exp=1767128169~hmac=8f9b91998ee62b5f9e03e0422e4ab3e945ea45058da48856213bbc5506d47caa&w=1480" alt="Biblioteca">
          </div>
        </div>
      </div>
    </section>

<section class="flow-section">
  
<div class="corner-circle-container">
        <svg class="dashed-circle" viewBox="0 0 500 500">
          <circle 
            cx="250" cy="250" r="240" 
            fill="none" 
            stroke="rgba(255,255,255,0.1)" 
            stroke-width="6" 
            stroke-linecap="round"     stroke-dasharray="20, 35"  />
        </svg>
      </div>

  <div class="flow-container">
    
    <div class="flow-left-visual">
      <div class="floating-interface-card">
        <div class="interface-header">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <div class="interface-body">
          <div class="skeleton-line full"></div>
          <div class="skeleton-line half"></div>
          <div class="skeleton-graph"></div>
        </div>
      </div>
    </div>

    <div class="flow-right-content">
      
      <div class="target-icon-card">
        <span class="check-icon">🎓</span>
      </div>

      <div class="flow-text-block">
        <h2>Do primeiro dia de aula<br>até o diploma na mão.</h2>
        <p>O GAM.py não apenas registra suas notas. Ele analisa seu desempenho para sugerir o momento exato de cursar optativas e quais matérias priorizar para evitar atrasos na formatura.</p>
      </div>

    </div>

  </div>
</section>

<section class="editorial-section">
      
      <div class="quote-symbol">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M14.017 21L14.017 18C14.017 16.8954 14.9124 16 16.017 16H19.017C19.5693 16 20.017 15.5523 20.017 15V9C20.017 8.44772 19.5693 8 19.017 8H15.017C14.4647 8 14.017 8.44772 14.017 9V11C14.017 11.5523 13.5693 12 13.017 12H12.017V5H22.017V15C22.017 18.3137 19.3307 21 16.017 21H14.017ZM5.01697 21L5.01697 18C5.01697 16.8954 5.9124 16 7.01697 16H10.017C10.5693 16 11.017 15.5523 11.017 15V9C11.017 8.44772 10.5693 8 10.017 8H6.01697C5.46468 8 5.01697 8.44772 5.01697 9V11C5.01697 11.5523 4.56925 12 4.01697 12H3.01697V5H13.017V15C13.017 18.3137 10.3307 21 7.01697 21H5.01697Z" fill="currentColor"/>
        </svg>
      </div>

      <div class="editorial-content">
        <blockquote>
          "O sucesso acadêmico não deve ser um mistério, mas sim uma ciência exata. Nosso objetivo não é apenas organizar grades, mas garantir que a jornada do aluno na universidade seja fluida."
        </blockquote>
      </div>

      <div class="author-block">
        
        <div class="author-visuals">
          <img src="https://placehold.co/100x100/6BA368/FFFFFF?text=GAM.py" alt="Foto do Autor" class="author-avatar">
          <div class="author-badge">
            <span>Coders</span>
          </div>
        </div>

        <div class="author-info">
          <cite>Equipe GAM.py</cite>
          <span class="author-role">Desenvolvedores do Projeto</span>
        </div>

      </div>

    </section>


    <section class="faq-section">
      <div class="faq-container">
        
        <div class="faq-header">
          <h2>Tire suas dúvidas<br>antes de começar.</h2>
        </div>

        <div class="faq-list">
          <div 
            v-for="(item, index) in faqItems" 
            :key="index" 
            class="faq-item"
            :class="{ 'active': item.isOpen }"
          >
            <button class="faq-question" @click="toggleFaq(index)">
              <span class="question-text">{{ item.question }}</span>
              <span class="icon-toggle">+</span>
            </button>

            <div class="faq-answer" v-show="item.isOpen">
              <div class="answer-inner">
                {{ item.answer }}
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <footer class="app-footer">
      <div class="footer-container">
        
        <div class="footer-brand">
          <img src="@/assets/logo.png" alt="GAM.py" class="footer-logo">
          <span>GAM.py &copy; 2025</span>
        </div>

        <div class="footer-links">
          <a href="https://github.com/allanasilvaf/Projetos_2" class="footer-link">
            GitHub
          </a>
          <a href="mailto:claudio.mendes@itec.ufpa.br" class="footer-link">
            Contato
          </a>
        </div>

      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      // FAQ
      faqItems: [
        { 
          question: 'Como faço meu primeiro acesso?', 
          answer: 'Crie sua conta utilizando o seu e-mail e senha e realize a configuração completa do seu perfil.',
          isOpen: false 
        },
        { 
          question: 'O sistema funciona offline?', 
          answer: 'A aplicação web possui um modo offline limitado para visualização de notas baixadas anteriormente (cache do navegador), mas requer internet para funcionar corretamente.',
          isOpen: false 
        },
        { 
          question: 'Como entro em contato com o suporte?', 
          answer: 'Dentro do painel do aluno, existe um ícone de "Ajuda" no canto inferior direito. Lá você pode abrir chamados diretamente para a TI da GAM.py.',
          isOpen: false 
        },
        // { 
        //   question: 'Posso integrar com o Google Agenda?', 
        //   answer: 'Sim! Vá em Ajustes > Integrações e conecte sua conta Google. Suas aulas e provas aparecerão automaticamente no seu calendário.',
        //   isOpen: false 
        // }
      ]
    }
  },
  methods: {

    scrollToFeatures() {
      const section = document.getElementById('funcionalidades');
      if (section) section.scrollIntoView({ behavior: 'smooth' });
    },

    toggleFaq(index) {

      this.faqItems[index].isOpen = !this.faqItems[index].isOpen;
      
      //  feche os outros p abrir um
      this.faqItems.forEach((item, i) => {
        if (i !== index) item.isOpen = false;
      });
    }
  }
}
</script>

<style scoped>

.home-content-wrapper {
  background-color: var(--color-bg-body);
}

.first-fold {
  height: calc(100vh - var(--header-height));
  width: 100%;
  
  position: relative; 
  
  display: flex;
  flex-direction: column;
  
  justify-content: center; 
  
  overflow: hidden;
  gap: 20px; 
}

.hero-section {
  flex-shrink: 0; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  
  padding: 0 20px;
  background: transparent;
  z-index: 1;
}
.hero-content {
  max-width: 900px;
  width: 100%;
  text-align: center;
}

.hero-badge-title {
  display: inline-block;
  background-color: var(--color-primary);
  color: white;
  padding: 10px 30px;
  border-radius: var(--radius-pill);
  margin-bottom: 25px;
  box-shadow: 0 4px 15px rgba(107, 163, 104, 0.3);
}
.hero-badge-title h1 {
  margin: 0;
  font-size: 2.2rem; 
  font-weight: 700;
  line-height: 1.2;
}
.hero-subtitle {
  color: var(--color-text-muted);
  font-size: 1.25rem; 
  margin: 0 auto;
  max-width: 700px;
  line-height: 1.6;
}

.main-grid-section {
  height: 45%;
  width: 100%;
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 20px;
  margin-bottom: 40px; 
  display: flex;
  flex-direction: column;
  z-index: 1;
}

.grid-container {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 2.5fr 1fr;
  gap: 20px;
}
.grid-image { width: 100%; height: 100%; object-fit: cover; border-radius: var(--radius-md); box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: transform 0.3s ease; display: block; }
.grid-image:hover { transform: scale(1.02); }
.grid-col-left.stacked-images { display: flex; flex-direction: column; gap: 15px; height: 100%; }
.img-half-height { flex: 1; height: 0; min-height: 0; }
.grid-col-center, .grid-col-right { height: 100%; border-radius: var(--radius-md); overflow: hidden; }
.img-full-height { height: 100%; }

.scroll-indicator-container {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}
.scroll-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  font-size: 1.4rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  display: flex; align-items: center; justify-content: center; animation: bounce 2s infinite;
  cursor: pointer;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* sessão de funcionalidades ===========================  */
.features-section {
  padding: 80px 20px;
  background-color: white;
  border-top-left-radius: 40px;
  border-top-right-radius: 40px;
  margin-top: -20px;
  box-shadow: 0 -10px 30px rgba(0,0,0,0.03);
}

.badge-container {
  text-align: center;
  margin-bottom: 20px;
}
.pill-badge {
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
  padding: 6px 16px;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.features-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px;
}
.features-header h2 {
  font-size: 2.5rem;
  color: var(--color-text-main);
  margin-bottom: 15px;
  line-height: 1.2;
}
.features-header p {
  font-size: 1.1rem;
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  max-width: var(--container-width);
  margin: 0 auto;
}

.feature-card {
  background-color: #f8f9fa;
  border-radius: 20px;
  padding: 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid transparent;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  border-color: var(--color-primary-light);
  background-color: white;
}

.card-text-area {
  flex: 1;
  padding-right: 15px;
}

.card-text-area h3 {
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: var(--color-text-main);
}

.card-text-area p {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  margin-bottom: 15px;
  line-height: 1.5;
}

.btn-card-action {
  background-color: var(--color-text-main);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.feature-card:hover .btn-card-action {
  background-color: var(--color-primary);
}

.card-visual-area img {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  object-fit: cover;
}

/* sessão com bola ===================================*/
.flow-section {
  position: relative; 
  background-color: #2C3E50; 
  color: white;
  padding: 100px 20px;
  overflow: hidden;
  min-height: 600px;
  display: flex;
  align-items: center;
}
.corner-circle-container {
  position: absolute;
  bottom: -10%;
  right: -5%;
  width: 45vw;  
  height: 45vw; 
  max-width: 600px;
  max-height: 600px;
  min-width: 300px;
  min-height: 300px;
  z-index: 0;
  pointer-events: none;
  animation: spin-slow 60s linear infinite;
}

.dashed-circle {
  width: 100%;
  height: 100%;
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}


.flow-container {
  width: 100%;
  max-width: var(--container-width);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  position: relative;
  z-index: 1;
}

.flow-left-visual {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 20px;
}

.floating-interface-card {
  background: white;
  width: 320px;
  height: 220px;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.interface-header { display: flex; gap: 6px; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.red { background: #ff5f56; }
.yellow { background: #ffbd2e; }
.green { background: #27c93f; }

.interface-body { flex: 1; display: flex; flex-direction: column; gap: 10px; }
.skeleton-line { height: 8px; background: #e0e0e0; border-radius: 4px; }
.full { width: 100%; }
.half { width: 60%; }
.skeleton-graph { flex: 1; background: #f0f4f4; border-radius: 8px; margin-top: 5px; border: 1px dashed #ccc; }


.flow-right-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding-left: 50px;
  
  backdrop-filter: blur(5px);
}

.target-icon-card {
  width: 60px;
  height: 60px;
  background: var(--color-primary);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  margin-bottom: 20px; 
}

.flow-text-block {
  text-align: left;
}

.flow-text-block h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 15px;
  line-height: 1.1;
}

.flow-text-block p {
  font-size: 1.1rem;
  opacity: 0.8;
  max-width: 400px;
  line-height: 1.6;
}

/* sessão de depoimento =========================== */
.editorial-section {
  background: linear-gradient(180deg, #eafaf1 0%, #ffffff 100%);
  
  padding: 100px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: var(--color-text-main);
}

.quote-symbol {
  color: var(--color-primary);
  opacity: 0.3;
  margin-bottom: 30px;
  transform: scale(1.5);
}

.editorial-content blockquote {
  font-family: 'Georgia', serif;
  font-size: 1.8rem;
  line-height: 1.6;
  max-width: 900px;
  margin: 0 auto 50px;
  color: #2c3e50;
  font-style: italic;
}

.highlight {
  color: var(--color-primary);
  font-weight: 700;
  font-style: normal;
  background: linear-gradient(120deg, transparent 0%, rgba(107, 163, 104, 0.15) 100%); /* Marca-texto sutil */
  padding: 0 5px;
}

.author-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.author-visuals {
  display: flex;
  align-items: center;
  gap: -15px;
}

.author-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  object-fit: cover;
  z-index: 2;
}

/* Selo Quadrado */
.author-badge {
  width: 40px;
  height: 40px;
  background-color: var(--color-text-main);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  font-weight: bold;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  border: 2px solid white;
  z-index: 1;
  margin-left: -15px;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-info cite {
  font-style: normal;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-text-main);
}

.author-role {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  letter-spacing: 1px;
}

/* sessão de perguntas =============================== */
.faq-section {
  padding: 100px 20px;
  background-color: white;
}

.faq-container {
  max-width: var(--container-width);
  margin: 0 auto;
}

.faq-header h2 {
  font-size: 3rem;
  color: var(--color-text-main);
  line-height: 1.1;
  margin-bottom: 60px;
  text-align: left;
}

.faq-list {
  display: flex;
  flex-direction: column;
  border-top: 1px solid #eee; /* Linha inicial */
}

.faq-item {
  border-bottom: 1px solid #eee; /* Linha separadora */
}

.faq-question {
  width: 100%;
  background: none;
  border: none;
  padding: 30px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
  transition: color 0.3s;
}

.faq-question:hover .question-text {
  color: var(--color-primary);
}

.question-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-main);
}

.icon-toggle {
  font-size: 2rem;
  font-weight: 300;
  color: var(--color-primary);
  transition: transform 0.3s ease;
  line-height: 1;
}

.faq-item.active .icon-toggle {
  transform: rotate(45deg);
  color: var(--color-danger);
}

.faq-answer {
  animation: slideDown 0.3s ease-out forwards;
}

.answer-inner {
  padding-bottom: 30px;
  padding-right: 50px;
  color: var(--color-text-muted);
  line-height: 1.6;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* footer ==================================== */
.app-footer {
  background-color: #1a252f;
  color: white;
  padding: 40px 20px;
}

.footer-container {
  max-width: var(--container-width);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 15px;
  font-weight: 700;
  opacity: 0.8;
}

.footer-logo {
  height: 30px;
  filter: grayscale(100%) brightness(200%);
}

.footer-links {
  display: flex;
  gap: 30px;
}

.footer-link {
  text-decoration: none;
  color: rgba(255,255,255,0.6);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s, transform 0.2s;
}

.footer-link:hover {
  color: white;
  transform: translateY(-2px);
}

/* media query para tela menor. falta arrumar!!!! :((( */

@media (max-width: 768px) {
  .faq-header h2 { font-size: 2rem; }
  
  .footer-container {
    flex-direction: column;
    gap: 30px;
  }
  
  .footer-links {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 768px) {
  .editorial-content blockquote {
    font-size: 1.4rem;
  }
}

@media (max-width: 900px) {
  .first-fold { height: auto; display: block; padding-bottom: 80px; }
  .hero-section { padding: 40px 20px; }
  .main-grid-section { height: 400px; margin-bottom: 20px; }
  .scroll-indicator-container { position: relative; bottom: auto; left: auto; transform: none; margin-top: 20px; }

.flow-container {
  grid-template-columns: 1fr;
  gap: 60px;
  }

.corner-circle-container {
  width: 80vw;
  height: 80vw;
  bottom: -10%;
  right: -20%;
  opacity: 0.5;
}

.flow-left-visual { align-items: center; padding-top: 0; }
.flow-right-content { padding-left: 0; text-align: center; align-items: center; }
.flow-text-block { text-align: center; }
.target-icon-card { transform: none; margin: 0 auto 20px; }
.connection-line { display: none; }
}
</style>