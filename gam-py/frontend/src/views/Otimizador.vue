<template>
  <div class="calc-container">
    <div class="calc-card">
      
      <div class="system-brand-premium">
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
            <input type="text" v-model="novaNota.codigo" placeholder="Código (Ex: MAT001)" class="flex-2">
            <input type="number" v-model.number="novaNota.valor" step="0.01" min="0" max="10" placeholder="Nota" class="flex-1">
            <button @click="adicionarAoHistorico" class="btn-add" :disabled="!isNotaValida">+</button>
          </div>
        </div>

        <div v-if="historicoNotas.length > 0" class="list-container">
          <div v-for="(item, index) in historicoNotas" :key="index" class="disc-row">
            <span class="disc-name"><strong>{{ item.codigo }}</strong></span>
            <div class="disc-details">
              <span class="nota-badge">{{ item.valor.toFixed(2) }}</span>
              <button @click="historicoNotas.splice(index, 1)" class="btn-del">✕</button>
            </div>
          </div>
        </div>

        <div class="action-footer-vertical">
          <div class="info-alert">
            <span class="icon">💡</span>
            <p>A ML cruzará os códigos das matérias que você já cursou para encontrar padrões de desempenho.</p>
          </div>
          <button 
            @click="gerarRecomendacao" 
            class="btn-primary btn-full" 
            :disabled="historicoNotas.length < 2 || loading"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Analisando Afinidades...' : 'Ver Sugestões de Matérias' }}
          </button>
        </div>
      </div>

      <div v-else class="results-container animate-pop">
        <h3 class="results-title">Sugestões para o Próximo Semestre:</h3>
        <p class="small-info text-center">Disciplinas com maior afinidade baseadas no seu perfil:</p>
        
        <div class="sugestao-grid">
          <div v-for="(sug, index) in recomendacoes" :key="index" class="sugestao-card">
            <div class="sugestao-header">
              <span class="prob-tag">Afinidade: {{ sug.afinidade }}%</span>
            </div>
            <h4>{{ sug.nome }}</h4>
            <p class="codigo-sub">{{ sug.codigo }}</p>
            <div class="progress-bar">
              <div class="progress" :style="{width: sug.afinidade + '%'}"></div>
            </div>
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
/* 1. Layout Base (Padronizado Verde GAM.py) */
.calc-container {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
  padding: 20px; font-family: sans-serif;
}

.calc-card {
  width: 100%; max-width: 700px; background: white; border-radius: 20px;
  padding: 65px 45px 45px; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  position: relative; overflow: hidden;
}

/* 2. Branding Superior */
.system-brand-premium {
  position: absolute; top: 0; left: 0; right: 0;
  height: 40px; background: #1e3020;
  display: flex; align-items: center; justify-content: center;
}

.code-icon { color: #4ade80; font-family: monospace; font-weight: bold; margin-right: 10px; }
.brand-text { color: white; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
.brand-highlight { color: #4ade80; }

/* 3. Tipografia e Cabeçalho */
.calc-header h1 { color: #2c5530; font-size: 26px; font-weight: 700; margin: 10px 0 8px; }
.subtitle { color: #666; font-size: 15px; margin-bottom: 0; line-height: 1.4; }
.divider { border: 0; height: 1px; background: #eee; margin: 25px 0 35px 0; }

.section-title { font-size: 14px; font-weight: 700; color: #2c5530; margin-bottom: 12px; text-align: left; }
.add-box { background: #f4f7f4; padding: 20px; border-radius: 12px; margin-bottom: 25px; }
.input-row { display: flex; gap: 10px; }
.flex-2 { flex: 2; } .flex-1 { flex: 1; }

input { 
  width: 100%; padding: 14px; border: 1.5px solid #eee; border-radius: 10px; 
  background: #fcfcfc; box-sizing: border-box; transition: all 0.3s;
}
input:focus { outline: none; border-color: #2c5530; background: white; }

/* 4. Listagem de Notas */
.list-container { max-height: 250px; overflow-y: auto; margin-bottom: 25px; }
.disc-row { 
  display: flex; justify-content: space-between; align-items: center; 
  padding: 12px 10px; border-bottom: 1px solid #f5f5f5; 
}
.disc-name { color: #333; font-size: 15px; }
.nota-badge { background: #e8f5e9; color: #2c5530; padding: 4px 12px; border-radius: 6px; font-weight: 700; }

/* 5. Botões */
.btn-primary { 
  background: #2c5530; color: white; border: none; border-radius: 12px; 
  font-weight: 700; cursor: pointer; transition: 0.3s; 
}
.btn-primary:hover:not(:disabled) { background: #3d7543; transform: translateY(-1px); }
.btn-full { width: 100%; padding: 18px; font-size: 16px; }

.btn-add { background: #13223f; color: white; border: none; width: 50px; border-radius: 10px; cursor: pointer; font-size: 22px; }
.btn-del { background: none; border: none; color: #ff5252; cursor: pointer; font-size: 16px; }

/* 6. Resultados do Otimizador */
.results-title { color: #2c5530; font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 5px; }
.small-info { color: #888; font-size: 13px; margin-bottom: 20px; }
.sugestao-grid { display: grid; grid-template-columns: 1fr; gap: 15px; margin: 20px 0; }
.sugestao-card { 
  background: #fcfdfc; border-left: 5px solid #4ade80; 
  padding: 18px; border-radius: 8px; text-align: left;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}
.sugestao-card h4 { color: #2c5530; margin: 5px 0; font-size: 17px; }
.codigo-sub { font-size: 12px; color: #999; margin-bottom: 10px; }
.prob-tag { font-size: 11px; font-weight: 800; color: #4a7c59; text-transform: uppercase; }

.progress-bar { width: 100%; height: 8px; background: #eee; border-radius: 10px; overflow: hidden; margin-top: 10px; }
.progress { height: 100%; background: #4ade80; transition: width 1s ease-in-out; }

.btn-back-full { 
  background: none; border: 1.5px solid #ddd; padding: 12px; width: 100%; 
  border-radius: 10px; color: #666; cursor: pointer; margin-top: 15px; font-weight: 600;
}

/* 7. Alertas e Utilitários */
.info-alert { 
  background: #e8f5e9; border-left: 4px solid #4ade80; 
  padding: 15px; border-radius: 8px; margin-bottom: 20px; 
  display: flex; gap: 12px; align-items: center; text-align: left;
}
.info-alert p { font-size: 13px; color: #2c5530; margin: 0; line-height: 1.4; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 0.8s linear infinite; display: inline-block; margin-right: 10px; }
@keyframes spin { to { transform: rotate(360deg); } }

button:disabled { background: #ccc !important; cursor: not-allowed; }
.text-center { text-align: center; }
</style>