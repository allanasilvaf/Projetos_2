<template>
  <div class="dashboard-container">
    <header class="dashboard-header text-center">
      <div class="welcome-text">
        <h1>Olá, {{ user ? user.nome.split(' ')[0] : 'Estudante' }}!</h1>
        <p>Aprenda a Gerenciar seu desempenho com as nossas funcionalidades</p>
      </div>
      <button @click="logout" class="btn-logout-floating" title="Sair do Sistema">
        <LogOut :size="20" />
      </button>
    </header>

    <main class="carousel-section">
      <div class="carousel-container">
        <div 
          v-for="(card, index) in features" 
          :key="index"
          class="feature-card"
          :class="{ 
            'active-card': activeIndex === index,
            'inactive-card': activeIndex !== index 
          }"
          @mouseenter="activeIndex = index"
        >
          <div class="card-icon-box">
            <component :is="card.icon" :size="38" class="icon-color" />
          </div>
          
          <div class="card-body">
            <h3>{{ card.title }}</h3>
            <p class="card-description">{{ card.description }}</p>
            
            <div class="how-to-use">
              <span class="usage-label">Modo de Uso</span>
              <p>{{ card.usage }}</p>
            </div>
          </div>

         <router-link v-if="card.route" :to="card.route" class="btn-card-launch">
          Acessar Ferramenta <ChevronRight :size="18" />
        </router-link>

        <a v-else :href="card.url" target="_blank" class="btn-card-launch">
          Abrir Chatbot <ChevronRight :size="18" />
        </a>
        </div>
      </div>

      <div class="carousel-indicators-container">
        <div class="carousel-indicators">
          <span 
            v-for="(_, i) in features" 
            :key="i" 
            :class="{ active: activeIndex === i }"
            @click="activeIndex = i"
          ></span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { Zap, Calculator, MessageSquare, LogOut, ChevronRight } from 'lucide-vue-next';

export default {
  name: 'Dashboard',
  components: { Zap, Calculator, MessageSquare, LogOut, ChevronRight },
  data() {
    return {
      user: null,
      activeIndex: 1,
      features: [
        {
          title: 'Otimizador de Grade',
          description: 'Análise preditiva de afinidade com matérias futuras.',
          usage: 'Baseado no seu histórico, nossa IA sugere as melhores disciplinas para sua próxima matrícula.',
          icon: 'Zap',
          route: '/otimizador'
        },
        {
          title: 'Calculadora de CRG',
          description: 'Previsão avançada do seu rendimento acadêmico total.',
          usage: 'Simule suas notas do semestre atual e veja o impacto real no seu CRG final.',
          icon: 'Calculator',
          route: '/calculadora'
        },
        {
          title: 'GAMBot AI',
          description: 'Seu tutor acadêmico disponível 24h via chat.',
          usage: 'Tire dúvidas sobre regras da universidade, ementas e receba dicas de estudo personalizadas.',
          icon: 'MessageSquare',
          url: 'https://gambot.streamlit.app/' 
        }
      ]
    }
  },
  mounted() {
    const userData = localStorage.getItem('user');
    if (userData) {
      this.user = JSON.parse(userData);
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: #f8fafc;
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* Centraliza o conteúdo verticalmente */
}

.dashboard-header {
  max-width: 800px;
  margin-bottom: 40px;
  position: relative;
  width: 100%;
}

.text-center { text-align: center; }

.welcome-text h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #2c5530;
  margin-bottom: 10px;
}

.welcome-text p {
  color: #64748b;
  font-size: 1.1rem;
}

/* Carrossel */
.carousel-section {
  width: 100%;
  max-width: 1200px;
}

.carousel-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: 100%;
  height: 520px;
}

.feature-card {
  background: white;
  width: 380px;
  height: 460px;
  padding: 40px;
  border-radius: 40px;
  display: flex;
  flex-direction: column;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  border: 1px solid #f1f5f9;
}

.active-card {
  width: 440px;
  height: 500px;
  opacity: 1;
  box-shadow: 0 40px 80px -15px rgba(44, 85, 48, 0.15);
  border-color: #dcfce7;
  z-index: 10;
}

.inactive-card {
  transform: scale(0.85);
  opacity: 0.5;
  filter: blur(1px);
}

.card-icon-box {
  width: 80px;
  height: 80px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  background: #f0fdf4;
}

.icon-color { color: #2c5530; }

.feature-card h3 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #2c5530;
  margin-bottom: 15px;
}

.card-description {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 25px;
}

.how-to-use {
  background: #f8fafc;
  padding: 20px;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
}

.usage-label {
  display: block;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  color: #2c5530;
  margin-bottom: 8px;
}

/* Ajuste nos Indicadores (PONTOS) */
.carousel-indicators-container {
  width: 100%;
  display: flex;
  justify-content: center; /* Centralização horizontal */
  margin-top: 30px;
}

.carousel-indicators {
  display: flex;
  gap: 12px;
}

.carousel-indicators span {
  width: 12px;
  height: 12px;
  background: #cbd5e1;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
}

.carousel-indicators span.active {
  background: #2c5530;
  width: 35px;
  border-radius: 10px;
}

.btn-card-launch {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  background: #2c5530;
  color: white;
  text-decoration: none;
  border-radius: 20px;
  font-weight: 700;
  transition: 0.3s;
}

.btn-logout-floating {
  position: absolute; right: 0; top: 0;
  background: white; border: 1px solid #e2e8f0;
  padding: 12px; border-radius: 50%; color: #94a3b8;
  cursor: pointer; transition: 0.3s;
}
</style>