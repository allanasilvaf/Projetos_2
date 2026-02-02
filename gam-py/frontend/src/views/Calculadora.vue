<template>
  <div class="calc-container">
    <div class="calc-card">
      
      <div class="system-brand-premium">
        <div class="brand-content">
          <span class="code-icon">‹/›</span>
          <span class="brand-text">Calculadora de CRG <span class="brand-highlight">- GAM.py</span></span>
        </div>
      </div>

      <div class="calc-header text-center">
        <h1>{{ step === 1 ? 'Histórico Acadêmico' : 'Matérias Atuais' }}</h1>
        <p class="subtitle">
          {{ step === 1 ? 'Informe seus dados acumulados até o semestre passado.' : 'Adicione as disciplinas que você está cursando agora.' }}
        </p>
      </div>

      <hr class="divider" />

      <div v-if="step === 1" class="step-content">
        <div class="form-grid-2">
          <div class="form-group">
            <label>CRG Atual</label>
            <input 
              type="number" 
              v-model.number="historico.crgAtual" 
              step="0.01"
              placeholder="0.00"
            >
          </div>
          <div class="form-group">
            <label>Carga Horária Total Cumprida</label>
            <input 
              type="number" 
              v-model.number="historico.chTotal"
              placeholder="0"
            >
          </div>
        </div>

        <div class="info-alert">
          <span class="icon">💡</span>
          <p><strong>Primeiro Semestre?</strong> Se você é calouro e não tem notas registradas, preencha os campos acima com <strong>0</strong>.</p>
        </div>
        
        <button 
          @click="step = 2" 
          class="btn-next" 
          :disabled="!isHistoricoPreenchido"
        >
          Prosseguir para Matérias Atuais →
        </button>
      </div>

      <div v-if="step === 2" class="step-content">
        <div class="add-box">
          <div class="input-row">
            <input type="text" v-model="novaDisc.nome" placeholder="Disciplina" class="flex-2">
            <input type="number" v-model.number="novaDisc.ch" placeholder="CH" class="flex-1">
            <select v-model="novaDisc.conceito" class="flex-1">
              <option value="" disabled selected>Conceito</option>
              <option value="EXC">EXC</option>
              <option value="BOM">BOM</option>
              <option value="REG">REG</option>
              <option value="INS">INS</option>
            </select>
            <button @click="adicionarDisciplina" class="btn-add" :disabled="!isNovaDiscValida">+</button>
          </div>
        </div>

        <div v-if="disciplinas.length > 0" class="list-container">
          <div v-for="(d, index) in disciplinas" :key="index" class="disc-row">
            <span class="disc-name"><strong>{{ index + 1 }}.</strong> {{ d.nome }}</span>
            <div class="disc-details">
              <span class="disc-ch">{{ d.ch }}h</span>
              <span class="disc-badge" :class="d.conceito">{{ d.conceito }}</span>
              <button @click="removerDisciplina(index)" class="btn-del">✕</button>
            </div>
          </div>
        </div>

        <div v-if="resultado" class="result-prediction">
          <p>Previsão Final do seu CRG:</p>
          <div class="val">{{ resultado }}</div>
          <small>Análise preditiva baseada no seu desempenho (Python ML)</small>
        </div>

        <div class="action-footer">
          <button @click="step = 1" class="btn-back">← Alterar Histórico</button>
          <button 
            @click="preverCRG" 
            class="btn-primary" 
            :disabled="disciplinas.length === 0 || loading"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Calculando...' : 'Gerar Previsão ML' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'CalculadoraCRG',
  data() {
    return {
      step: 1,
      loading: false,
      resultado: null,
      historico: { 
        crgAtual: null, 
        chTotal: null 
      },
      novaDisc: { 
        nome: '', 
        ch: null, 
        conceito: '' 
      },
      disciplinas: []
    }
  },
  computed: {
    isHistoricoPreenchido() {
      return this.historico.crgAtual !== null && this.historico.chTotal !== null;
    },
    isNovaDiscValida() {
      return this.novaDisc.nome.trim() !== '' && this.novaDisc.ch > 0 && this.novaDisc.conceito !== '';
    }
  },
  methods: {
    adicionarDisciplina() {
      if (this.isNovaDiscValida) {
        this.disciplinas.push({ ...this.novaDisc });
        this.novaDisc = { nome: '', ch: null, conceito: '' };
        this.resultado = null;
      }
    },
    removerDisciplina(index) {
      this.disciplinas.splice(index, 1);
      this.resultado = null;
    },
    async preverCRG() {
      this.loading = true;
      // Simulando a chamada para o script Python
      setTimeout(() => {
        const mockRes = (Math.random() * (9.5 - 7.0) + 7.0).toFixed(2);
        this.resultado = mockRes;
        this.loading = false;
      }, 1500);
    }
  }
}
</script>

<style scoped>
.calc-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
  padding: 20px;
  font-family: sans-serif;
}

.calc-card {
  width: 100%;
  max-width: 750px;
  background: white;
  border-radius: 20px;
  padding: 65px 45px 45px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  position: relative;
  overflow: hidden;
}

/* HEADER SUPERIOR */
.system-brand-premium {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: #1e3020;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
}

.code-icon { color: #4ade80; font-family: monospace; font-weight: bold; margin-right: 10px; }
.brand-text { color: #ffffff; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.brand-highlight { color: #4ade80; }

.text-center { text-align: center; }
.calc-header h1 { color: #2c5530; font-size: 26px; font-weight: 700; margin-bottom: 8px; margin-top: 10px;}
.subtitle { color: #666; font-size: 15px; margin-bottom: 0; }
.divider { border: 0; height: 1px; background: #eee; margin: 25px 0 35px 0; }

.form-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }
.form-group label { display: block; margin-bottom: 10px; font-size: 14px; font-weight: 600; color: #444; text-align: left; }

input, select { width: 100%; padding: 14px; border: 1.5px solid #eee; border-radius: 10px; background: #fcfcfc; box-sizing: border-box; }

.info-alert {
  background: #fff8e1;
  border-left: 4px solid #ffc107;
  padding: 15px;
  margin-bottom: 25px;
  border-radius: 8px;
  display: flex;
  gap: 12px;
  align-items: center;
}
.info-alert p { font-size: 13px; color: #856404; margin: 0; text-align: left; line-height: 1.4; }

.add-box { background: #f4f7f4; padding: 20px; border-radius: 12px; margin-bottom: 25px; }
.input-row { display: flex; gap: 10px; }
.flex-2 { flex: 2; } 
.flex-1 { flex: 1; }

.btn-add { background: #2c5530; color: white; border: none; padding: 0 20px; border-radius: 10px; cursor: pointer; font-size: 22px; transition: 0.2s; }
.btn-add:hover { background: #3d7543; }

.disc-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 5px; border-bottom: 1px solid #f5f5f5; }
.disc-badge { padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 11px; }
.EXC { background: #e8f5e9; color: #2e7d32; }
.BOM { background: #e3f2fd; color: #1565c0; }
.REG { background: #fffde7; color: #fbc02d; }
.INS { background: #ffebee; color: #c62828; }

.btn-del { background: none; border: none; color: #ff5252; cursor: pointer; font-size: 16px; padding-left: 10px; }

.result-prediction { margin-top: 30px; padding: 25px; background: #f0f7f0; border: 2.5px dashed #2c5530; border-radius: 15px; text-align: center; }
.result-prediction .val { font-size: 50px; font-weight: 900; color: #2c5530; margin: 10px 0; }

.action-footer { display: flex; justify-content: space-between; margin-top: 30px; align-items: center;}
.btn-primary { background: #2c5530; color: white; padding: 16px 30px; border: none; border-radius: 12px; cursor: pointer; font-weight: 700; }
.btn-next { width: 100%; background: #2c5530; color: white; padding: 18px; border: none; border-radius: 12px; cursor: pointer; font-weight: 700; font-size: 16px; }
.btn-back { background: none; border: 1px solid #ddd; padding: 10px 20px; border-radius: 10px; cursor: pointer; color: #888; font-size: 14px;}

button:disabled { background: #ccc !important; cursor: not-allowed; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 0.8s linear infinite; display: inline-block; margin-right: 10px; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>