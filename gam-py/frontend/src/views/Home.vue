<template>
  <div class="home-container bg-bg-body overflow-x-hidden">

    <div class="relative h-[calc(100vh-80px)] flex flex-col justify-between pt-10 pb-4 gap-6 px-4 md:px-0">
      
      <section class="flex flex-col items-center text-center px-4 z-10 shrink-0">
        <div class="bg-primary text-white px-8 py-3 rounded-full font-extrabold shadow-xl shadow-green-500/20 mb-5 transform hover:scale-105 transition-transform text-xl md:text-2xl tracking-tight">
          <h1>Assuma o controle da sua graduação!</h1>
        </div>
        <p class="text-gray-600 text-xl md:text-3xl font-medium max-w-3xl leading-snug">
          Acompanhe seu CRG, gerencie faltas e planeje o semestre ideal em um único lugar.
        </p>
      </section>

      <main class="w-full max-w-6xl mx-auto px-4 flex-1 min-h-0 z-10">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 h-full items-center">
          
          <div class="hidden md:flex flex-col gap-4 h-full justify-center py-4">
            <img src="@/assets/img-1.png" class="flex-1 w-full h-0 object-cover rounded-2xl shadow-sm hover:scale-[1.02] transition-transform rotate-[-2deg]">
            <img src="@/assets/img-2.png" class="flex-1 w-full h-0 object-cover rounded-2xl shadow-sm hover:scale-[1.02] transition-transform rotate-[-2deg]">
          </div>

          <div class="col-span-1 md:col-span-2 h-full py-2">
            <img src="@/assets/img-3.png" class="w-full h-full object-cover rounded-3xl shadow-md hover:scale-[1.01] transition-transform z-20 relative">
          </div>

          <div class="hidden md:block h-full py-4">
            <img src="@/assets/img-4.png" class="w-full h-full object-cover rounded-2xl shadow-sm hover:scale-[1.02] transition-transform rotate-[2deg]">
          </div>

        </div>
      </main>

      <div class="flex justify-center shrink-0 z-10">
        <button @click="scrollToFeatures" class="w-12 h-12 rounded-full bg-white border-2 border-primary text-primary flex items-center justify-center shadow-md animate-bounce hover:bg-primary hover:text-white transition-colors cursor-pointer">
          <ArrowDown :size="24" stroke-width="2.5" />
        </button>
      </div>
    </div>

    <section id="funcionalidades" class="bg-white rounded-t-[50px] py-24 px-6 -mt-8 shadow-[0_-10px_40px_rgba(0,0,0,0.05)] relative z-20">
      
      <div class="text-center mb-16">
        <span class="bg-green-100 text-primary font-bold px-4 py-1 rounded-full text-sm uppercase tracking-wider">
          Recursos Exclusivos
        </span>
        <h2 class="text-3xl md:text-4xl font-bold text-dark mt-4 mb-4">
          Inteligência de Dados na sua Graduação
        </h2>
        <p class="text-gray-500 max-w-2xl mx-auto text-lg">
          Utilize métricas precisas para prever seu desempenho e garantir sua formação no tempo certo.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto">
        
        <div class="group bg-gray-50 rounded-3xl p-6 flex items-center justify-between hover:-translate-y-2 hover:bg-white hover:shadow-xl hover:border-green-200 border border-transparent transition-all duration-300">
          <div class="flex-1 pr-4">
            <h3 class="text-xl font-bold text-dark mb-2">Calculadora CRG</h3>
            <p class="text-gray-500 text-sm mb-4">Simule seu coeficiente final com base nas notas parciais.</p>
            <router-link to="/dashboard" class="inline-block bg-dark text-white px-4 py-2 rounded-full text-xs font-bold group-hover:bg-primary transition-colors">
              Simular Agora
            </router-link>
          </div>
          <img src="https://img.freepik.com/fotos-gratis/close-up-da-mao-usando-uma-calculadora_1220-58.jpg" class="w-24 h-24 rounded-xl object-cover shadow-sm">
        </div>

        <div class="group bg-gray-50 rounded-3xl p-6 flex items-center justify-between hover:-translate-y-2 hover:bg-white hover:shadow-xl hover:border-green-200 border border-transparent transition-all duration-300">
          <div class="flex-1 pr-4">
            <h3 class="text-xl font-bold text-dark mb-2">Otimizador</h3>
            <p class="text-gray-500 text-sm mb-4">Recomendações inteligentes das melhores disciplinas.</p>
            <router-link to="/dashboard" class="inline-block bg-dark text-white px-4 py-2 rounded-full text-xs font-bold group-hover:bg-primary transition-colors">
              Montar Grade
            </router-link>
          </div>
          <img src="https://img.freepik.com/fotos-gratis/jigsaw-trabalho-em-equipe-conceito-tiro-macro_53876-17929.jpg" class="w-24 h-24 rounded-xl object-cover shadow-sm">
        </div>

        <div class="group bg-gray-50 rounded-3xl p-6 flex items-center justify-between hover:-translate-y-2 hover:bg-white hover:shadow-xl hover:border-green-200 border border-transparent transition-all duration-300">
          <div class="flex-1 pr-4">
            <h3 class="text-xl font-bold text-dark mb-2">Desempenho</h3>
            <p class="text-gray-500 text-sm mb-4">Gráficos detalhados sobre seu progresso acadêmico.</p>
            <router-link to="/dashboard" class="inline-block bg-dark text-white px-4 py-2 rounded-full text-xs font-bold group-hover:bg-primary transition-colors">
              Ver Relatório
            </router-link>
          </div>
          <img src="https://img.freepik.com/fotos-gratis/alto-angulo-de-dardo-na-mosca_23-2148443764.jpg" class="w-24 h-24 rounded-xl object-cover shadow-sm">
        </div>

      </div>
    </section>

    <section class="relative bg-dark text-white py-24 px-6 overflow-hidden">
      <div class="absolute -bottom-1/4 -right-10 w-[500px] h-[500px] border-[6px] border-white/10 border-dashed rounded-full animate-spin-slow pointer-events-none"></div>
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center relative z-10">
        <div class="flex justify-center">
          <div class="bg-white w-80 h-56 rounded-2xl shadow-2xl p-4 flex flex-col gap-4 animate-float text-gray-800">
            <div class="flex gap-2">
              <div class="w-3 h-3 rounded-full bg-red-400"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
              <div class="w-3 h-3 rounded-full bg-green-400"></div>
            </div>
            <div class="h-2 bg-gray-200 rounded w-full"></div>
            <div class="h-2 bg-gray-200 rounded w-2/3"></div>
            <div class="flex-1 bg-gray-50 border border-dashed border-gray-300 rounded-lg mt-2"></div>
          </div>
        </div>
        <div class="text-center md:text-left">
          <div class="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center text-3xl mb-6 shadow-lg mx-auto md:mx-0">
            🎓
          </div>
          <h2 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">Do primeiro dia<br>até o diploma.</h2>
          <p class="text-gray-400 text-lg leading-relaxed max-w-md mx-auto md:mx-0">
            O GAM.py não apenas registra suas notas. Ele analisa seu desempenho para sugerir o momento exato de cursar optativas.
          </p>
        </div>
      </div>
    </section>

    <section class="py-24 px-6 bg-gradient-to-b from-green-50 to-white text-center">
      <div class="max-w-4xl mx-auto flex flex-col items-center">
        <Quote :size="60" class="text-primary/30 mb-8" />
        <blockquote class="text-2xl md:text-3xl font-serif italic text-dark leading-relaxed mb-12">
          "O sucesso acadêmico não deve ser um mistério, mas sim uma ciência exata. Nosso objetivo é garantir que a jornada do aluno seja fluida."
        </blockquote>
        <div class="flex flex-col items-center">
          <div class="relative mb-4">
            <img src="https://placehold.co/100x100/6BA368/FFFFFF?text=GAM" class="w-20 h-20 rounded-full border-4 border-white shadow-md object-cover relative z-10">
            <div class="absolute -bottom-2 -right-2 bg-dark text-white text-[10px] font-bold px-2 py-1 rounded-md z-20 border-2 border-white">DEVS</div>
          </div>
          <cite class="not-italic font-bold text-lg text-dark">Equipe GAM.py</cite>
          <span class="text-gray-500 text-sm tracking-widest uppercase">Desenvolvedores UFPA</span>
        </div>
      </div>
    </section>

    <section class="py-20 px-6 bg-white max-w-4xl mx-auto">
      <h2 class="text-3xl md:text-4xl font-bold text-dark mb-12 text-center md:text-left">
        Tire suas dúvidas<br>antes de começar.
      </h2>
      <div class="border-t border-gray-100">
        <div v-for="(item, index) in faqItems" :key="index" class="border-b border-gray-100">
          <button @click="toggleFaq(index)" class="w-full py-8 flex justify-between items-center text-left hover:text-primary transition-colors group">
            <span class="text-lg md:text-xl font-semibold text-dark group-hover:text-primary">{{ item.question }}</span>
            <span class="text-2xl font-light text-primary transition-transform duration-300" :class="{ 'rotate-45 text-red-500': item.isOpen }">
              <Plus v-if="!item.isOpen" />
              <X v-else />
            </span>
          </button>
          <div v-show="item.isOpen" class="pb-8 pr-8 text-gray-500 leading-relaxed animate-fade-in-down">
            {{ item.answer }}
          </div>
        </div>
      </div>
    </section>

    <footer class="bg-gray-900 text-white py-12 px-6">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-4 opacity-80">
          <img src="@/assets/logo.png" alt="GAM.py" class="h-8 grayscale brightness-200">
          <span class="font-bold">GAM.py &copy; 2026</span>
        </div>
        <div class="flex gap-8 text-sm text-gray-400">
          <a href="https://github.com/allanasilvaf/Projetos_2" target="_blank" class="hover:text-white transition-colors flex items-center gap-2">
            <Github :size="16" /> GitHub
          </a>
          <a href="mailto:claudio.mendes@itec.ufpa.br" class="hover:text-white transition-colors flex items-center gap-2">
            <Mail :size="16" /> Contato
          </a>
        </div>
      </div>
    </footer>

  </div>
</template>

<script>
import { ArrowDown, Quote, Plus, X, Github, Mail } from 'lucide-vue-next';

export default {
  name: 'HomeView',
  components: {
    ArrowDown, Quote, Plus, X, Github, Mail
  },
  data() {
    return {
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
        }
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
      this.faqItems.forEach((item, i) => {
        if (i !== index) item.isOpen = false;
      });
    }
  }
}
</script>

<style scoped>
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow {
  animation: spin-slow 60s linear infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-down {
  animation: fadeInDown 0.3s ease-out forwards;
}
</style>