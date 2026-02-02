<template>
  <div class="calc-container">
    <div class="calc-card">
      
      <div class="system-brand-premium brand-optimizer">
        <div class="brand-content">
          <span class="code-icon">⚡</span>
          <span class="brand-text">Otimizador de Grade <span class="brand-highlight">- GAM.py</span></span>
        </div>
      </div>

      <div class="calc-header text-center">
        <h1>Coleta de Notas</h1>
        <p class="subtitle">Insira suas notas anteriores para calcular sua afinidade com as próximas matérias.</p>
      </div>

      <hr class="divider" />

      <div v-if="!processado" class="step-content">
        <div class="add-box">
          <p class="section-title">Adicionar Matéria Concluída:</p>
          <div class="input-row">
            <input type="text" v-model="novaNota.codigo" placeholder="Código (Ex: MAT001)" class="flex-1">
            <input type="number" v-model.number="novaNota.valor" step="0.01" min="0" max="10" placeholder="Nota (Ex: 8.50)" class="flex-1">
            <button @click="adicionarAoHistorico" class="btn-add" :disabled="!isNotaValida">+</button>
          </div>
        </div>

        <div v-if="historicoNotas.length > 0" class="list-container">
          <div v-for="(item, index) in historicoNotas" :key="index" class="disc-row">
            <span><strong>{{ item.codigo }}</strong></span>
            <span class="nota-badge">{{ item.valor.toFixed(2) }}</span>
            <button @click="historicoNotas.splice(index, 1)" class="btn-del">✕</button>
          </div>
        </div>

        <div class="action-footer">
          <div class="info-alert">
            <p>💡 A ML cruzará os códigos das matérias que você já cursou para encontrar padrões de desempenho.</p>
          </div>
          <button 
            @click="gerarRecomendacao" 
            class="btn-optimizer" 
            :disabled="historicoNotas.length < 2 || loading"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Analisando Afinidades...' : 'Ver Sugestões de Matérias' }}
          </button>
        </div>
      </div>

      <div v-else class="results-container">
        <h3>Sugestões para o Próximo Semestre:</h3>
        <p class="small-info">Disciplinas com maior probabilidade de sucesso baseadas no seu perfil:</p>
        
        <div class="sugestao-grid">
          <div v-for="(sug, index) in recomendacoes" :key="index" class="sugestao-card">
            <div class="sugestao-header">
              <span class="prob-tag">Afinidade: {{ sug.afinidade }}%</span>
            </div>
            <h4>{{ sug.nome }}</h4>
            <p class="codigo-sub">{{ sug.codigo }}</p>
            <div class="progress-bar"><div class="progress" :style="{width: sug.afinidade + '%'}"></div></div>
          </div>
        </div>

        <button @click="processado = false" class="btn-back-full">← Editar meu histórico</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Otimizador',
  data() {
    return {
      loading: false,
      processado: false,
      novaNota: { codigo: '', valor: null },
      historicoNotas: [],
      recomendacoes: []
    }
  },
  computed: {
    isNotaValida() {
      return this.novaNota.codigo.trim() && this.novaNota.valor >= 0 && this.novaNota.valor <= 10;
    }
  },
  methods: {
    adicionarAoHistorico() {
      this.historicoNotas.push({ ...this.novaNota });
      this.novaNota = { codigo: '', valor: null };
    },
    async gerarRecomendacao() {
      this.loading = true;
      // Simulando a rede neural processando as notas (Ex: 7.55, 8.00...)
      setTimeout(() => {
        this.recomendacoes = [
          { codigo: 'INF003', nome: 'Algoritmos Avançados', afinidade: 94 },
          { codigo: 'MAT005', nome: 'Estatística Aplicada', afinidade: 88 },
          { codigo: 'ENG002', nome: 'Circuitos Lógicos', afinidade: 72 }
        ];
        this.processado = true;
        this.loading = false;
      }, 2000);
    }
  }
}
</script>

<style scoped>
/* Estilo base mantendo a Calculadora */
.calc-container {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 20px; font-family: sans-serif;
}

.calc-card {
  width: 100%; max-width: 700px; background: white; border-radius: 20px;
  padding: 65px 40px 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  position: relative; overflow: hidden;
}

.system-brand-premium.brand-optimizer {
  background: #0f1c2e; position: absolute; top: 0; left: 0; right: 0;
  height: 40px; display: flex; align-items: center; justify-content: center;
}

.code-icon { color: #00d2ff; font-family: monospace; font-weight: bold; margin-right: 10px; }
.brand-text { color: white; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.brand-highlight { color: #00d2ff; }

.section-title { font-size: 14px; font-weight: 700; color: #1e3c72; margin-bottom: 10px; text-align: left; }
.input-row { display: flex; gap: 10px; margin-bottom: 15px; }
.flex-1 { flex: 1; }

.nota-badge { background: #e3f2fd; color: #1e3c72; padding: 4px 12px; border-radius: 6px; font-weight: 700; }

.btn-optimizer {
  width: 100%; background: #1e3c72; color: white; padding: 18px; border: none;
  border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.3s;
}

.sugestao-grid { display: grid; grid-template-columns: 1fr; gap: 15px; margin: 20px 0; }
.sugestao-card { background: #f8fbff; border-left: 5px solid #00d2ff; padding: 15px; border-radius: 8px; text-align: left; }
.codigo-sub { font-size: 12px; color: #888; margin-bottom: 10px; }
.prob-tag { font-size: 11px; font-weight: 800; color: #1e3c72; text-transform: uppercase; }

.progress-bar { width: 100%; height: 6px; background: #eee; border-radius: 10px; overflow: hidden; }
.progress { height: 100%; background: #00d2ff; transition: width 1s ease-in-out; }

.btn-back-full { background: none; border: 1px solid #ddd; padding: 10px; width: 100%; border-radius: 8px; color: #666; cursor: pointer; margin-top: 10px; }

/* REUSANDO OS ESTILOS DA CALCULADORA */
.calc-header h1 { color: #1e3c72; font-size: 24px; font-weight: 700; margin-bottom: 10px; }
.subtitle { color: #666; font-size: 14px; margin-bottom: 20px; }
.divider { border: 0; height: 1px; background: #eee; margin: 20px 0; }
.add-box { background: #f4f7f4; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
.btn-add { background: #1e3c72; color: white; border: none; padding: 0 20px; border-radius: 10px; cursor: pointer; font-size: 22px; }
.disc-row { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
.btn-del { background: none; border: none; color: #ff5252; cursor: pointer; font-size: 16px; }
.info-alert { background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 8px; margin-bottom: 15px; text-align: left; font-size: 13px; color: #1e3c72; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 0.8s linear infinite; display: inline-block; margin-right: 10px; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>