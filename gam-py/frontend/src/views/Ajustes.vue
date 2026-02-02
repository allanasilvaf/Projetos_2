<template>
  <div class="min-h-screen bg-gray-50 p-6 font-poppins">
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <div class="lg:col-span-2 space-y-8">
        
        <div class="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 flex justify-between items-center">
          <div>
            <h1 class="text-2xl font-bold text-dark mb-2">Olá, {{ user.nome || 'Estudante' }}! 👋</h1>
            <p class="text-gray-500">Aqui está o resumo do seu desempenho acadêmico.</p>
          </div>
          <div class="hidden md:block">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-primary font-bold text-xl">
              {{ user.nome ? user.nome.charAt(0) : 'U' }}
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-primary transition-colors cursor-pointer group">
            <div class="flex items-center gap-3 mb-2">
              <div class="p-2 bg-blue-50 text-blue-600 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition-colors">
                <Activity :size="20" />
              </div>
              <span class="font-bold text-gray-600 text-sm">CRG Atual</span>
            </div>
            <p class="text-3xl font-bold text-dark">8.45</p>
          </div>

          <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-primary transition-colors cursor-pointer group">
            <div class="flex items-center gap-3 mb-2">
              <div class="p-2 bg-purple-50 text-purple-600 rounded-lg group-hover:bg-purple-600 group-hover:text-white transition-colors">
                <Clock :size="20" />
              </div>
              <span class="font-bold text-gray-600 text-sm">Horas Cursadas</span>
            </div>
            <p class="text-3xl font-bold text-dark">1.240h</p>
          </div>

          <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-primary transition-colors cursor-pointer group">
            <div class="flex items-center gap-3 mb-2">
              <div class="p-2 bg-orange-50 text-orange-600 rounded-lg group-hover:bg-orange-600 group-hover:text-white transition-colors">
                <AlertCircle :size="20" />
              </div>
              <span class="font-bold text-gray-600 text-sm">Faltas (Semestre)</span>
            </div>
            <p class="text-3xl font-bold text-dark">4</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
           <button class="p-4 bg-white rounded-xl border border-gray-200 text-left hover:shadow-md transition-all flex items-center gap-3">
             <Calculator class="text-primary" /> Simular CRG
           </button>
           <button class="p-4 bg-white rounded-xl border border-gray-200 text-left hover:shadow-md transition-all flex items-center gap-3">
             <LayoutGrid class="text-primary" /> Otimizar Grade
           </button>
        </div>

      </div>

      <div class="space-y-6">
        
        <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
          <h2 class="text-lg font-bold text-dark mb-4 flex items-center gap-2">
            <User :size="20" class="text-primary" /> Dados Pessoais
          </h2>
          
          <div class="space-y-4">
            <div>
              <label class="text-xs font-bold text-gray-400 uppercase">Nome Completo</label>
              <input type="text" v-model="user.nome" class="w-full mt-1 p-2 bg-gray-50 border border-gray-200 rounded-lg text-dark font-medium focus:border-primary outline-none" placeholder="Seu nome">
            </div>
            
            <div>
              <label class="text-xs font-bold text-gray-400 uppercase">E-mail</label>
              <input type="email" v-model="user.email" class="w-full mt-1 p-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-500" readonly>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs font-bold text-gray-400 uppercase">Matrícula</label>
                <input type="text" v-model="user.matricula" class="w-full mt-1 p-2 bg-gray-50 border border-gray-200 rounded-lg text-dark font-medium focus:border-primary outline-none">
              </div>
              <div>
                <label class="text-xs font-bold text-gray-400 uppercase">Curso</label>
                <input type="text" v-model="user.curso" class="w-full mt-1 p-2 bg-gray-50 border border-gray-200 rounded-lg text-dark font-medium focus:border-primary outline-none">
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 relative overflow-hidden">
          <h2 class="text-lg font-bold text-dark mb-4 flex items-center gap-2 relative z-10">
            <PlusCircle :size="20" class="text-primary" /> Adicionar Manualmente
          </h2>

          <form @submit.prevent="addManualDiscipline" class="relative z-10">
            
            <!-- Nome da Matéria -->
            <div class="form-group mb-4">
              <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">Nome da Matéria</label>
              <div class="input-wrapper relative">
                <svg class="input-icon absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <input type="text" v-model="manualForm.nome" placeholder="Ex: Cálculo I" required class="custom-input">
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3 mb-4">
              <!-- Conceito -->
              <div class="form-group">
                <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">Conceito</label>
                <div class="input-wrapper relative">
                  <svg class="input-icon absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <select v-model="manualForm.conceito" required class="custom-input appearance-none">
                    <option value="EXCELENTE">Excelente</option>
                    <option value="BOM">Bom</option>
                    <option value="REGULAR">Regular</option>
                    <option value="INSUFICIENTE">Insuficiente</option>
                  </select>
                </div>
              </div>

              <!-- Situação -->
              <div class="form-group">
                <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">Situação</label>
                <div class="input-wrapper relative">
                  <svg class="input-icon absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <select v-model="manualForm.situacao" required class="custom-input appearance-none">
                    <option value="APROVADO">Aprovado</option>
                    <option value="REPROVADO">Reprovado</option>
                    <option value="MATRICULADO">Cursando</option>
                  </select>
                </div>
              </div>
            </div>

            <button type="submit" class="w-full py-3 bg-gradient-to-br from-[#2c5530] to-[#4a7c59] text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2">
              <PlusCircle :size="18" /> Adicionar à Lista
            </button>
          </form>
        </div>

        <div class="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 bg-gray-50/50">
            <h2 class="text-lg font-bold text-dark flex items-center gap-2">
              <FileText :size="20" class="text-primary" /> Importar Histórico
            </h2>
            <p class="text-xs text-gray-500 mt-1">Envie o PDF do SIGAA para atualizar suas notas.</p>
          </div>

          <div v-if="!parsedData.length" class="p-6">
            <div 
              class="border-2 border-dashed border-gray-300 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer hover:bg-green-50 hover:border-primary transition-all group relative text-center"
              @dragover.prevent
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <input type="file" ref="fileInput" accept=".pdf" class="hidden" @change="handleFileSelect">
              <UploadCloud :size="32" class="text-gray-400 group-hover:text-primary mb-3 transition-colors" />
              <p class="text-sm font-bold text-gray-600">Clique ou arraste o PDF</p>
              
              <div v-if="loading" class="absolute inset-0 bg-white/90 flex flex-col items-center justify-center z-10 rounded-2xl">
                <Loader2 :size="30" class="animate-spin text-primary mb-2" />
                <span class="text-xs font-bold text-primary">Lendo...</span>
              </div>
            </div>
          </div>

          <div v-else class="p-0">
            <div class="max-h-[400px] overflow-y-auto custom-scrollbar border-b border-gray-100">
              <table class="w-full text-sm text-left">
                <thead class="bg-gray-50 text-gray-500 uppercase font-bold text-[10px] sticky top-0 z-10">
                  <tr>
                    <th class="px-4 py-2">Matéria</th>
                    <th class="px-2 py-2">Conceito</th>
                    <th class="px-2 py-2">Nota</th>
                    <th class="px-2 py-2 text-center">Ação</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="(item, index) in parsedData" :key="index" class="hover:bg-gray-50">
                    <td class="px-4 py-2 font-mono font-bold text-primary text-xs">
                      {{ item.id_materia }}
                    </td>
                    <td class="px-2 py-2">
                      <select 
                        v-model="item.conceito"
                        @change="updateNotaFromConcept(item)"
                        class="bg-transparent font-bold text-xs outline-none cursor-pointer"
                        :class="getConceptColor(item.conceito)"
                      >
                        <option value="E">E</option>
                        <option value="B">B</option>
                        <option value="R">R</option>
                        <option value="I">I</option>
                        <option value="S">S</option>
                      </select>
                    </td>
                    <td class="px-2 py-2">
                      <input 
                        type="number" 
                        v-model.number="item.nota" 
                        step="0.1" min="0" max="10"
                        class="w-12 bg-gray-50 border border-gray-200 rounded px-1 py-0.5 text-center font-mono text-xs focus:border-primary outline-none"
                      >
                    </td>
                    <td class="px-2 py-2 text-center">
                      <button @click="removeLine(index)" class="text-gray-300 hover:text-red-500">
                        <Trash2 :size="14" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="p-4 flex gap-2 justify-end bg-gray-50">
              <button @click="parsedData = []" class="px-4 py-2 text-xs font-bold text-gray-500 hover:text-dark">Cancelar</button>
              <button @click="saveData" class="px-4 py-2 bg-primary text-white rounded-lg text-xs font-bold hover:bg-green-700 flex items-center gap-2">
                <CheckCircle :size="14" /> Salvar
              </button>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
import { 
  Settings, UploadCloud, Loader2, Trash2, CheckCircle, PlusCircle,
  User, FileText, Activity, Clock, AlertCircle, Calculator, LayoutGrid 
} from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'PerfilView',
  components: { 
    Settings, UploadCloud, Loader2, Trash2, CheckCircle, PlusCircle,
    User, FileText, Activity, Clock, AlertCircle, Calculator, LayoutGrid 
  },
  data() {
    return {
      loading: false,
      parsedData: [],
      user: {
        nome: '',
        email: '',
        matricula: '',
        curso: 'Engenharia da Computação'
      },
      // Formulário Manual
      manualForm: {
        nome: '',
        conceito: 'EXCELENTE',
        situacao: 'APROVADO'
      }
    }
  },
  mounted() {
    // Carrega dados do usuário do localStorage (simulação)
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        this.user = { ...this.user, ...parsed };
      } catch (e) { console.error("Erro ao ler usuário", e); }
    }
  },
  methods: {
    handleFileSelect(e) {
      if (e.target.files && e.target.files[0]) {
        this.processFile(e.target.files[0]);
      }
    },
    
    handleDrop(e) {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.processFile(e.dataTransfer.files[0]);
      }
    },

    async processFile(file) {
      this.loading = true;

      if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) {
         alert('Por favor, envie apenas arquivos PDF.');
         this.loading = false;
         return;
      }

      const formData = new FormData();
      formData.append('file', file); 

      try {
        const response = await api.post('/api/parse-historico', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.parsedData = response.data.map(item => ({
          ...item,
          nota: this.convertConceptToGrade(item.conceito)
        }));
        
        if (this.parsedData.length === 0) {
          alert("Nenhuma disciplina encontrada. Verifique se o PDF é o Histórico Oficial do SIGAA.");
        }

      } catch (error) {
        console.error("Erro na integração:", error);
        
        if (error.response) {
          alert(`Erro: ${error.response.data.detail || 'Falha ao processar arquivo'}`);
        } else if (error.request) {
          alert("Erro de conexão: Verifique se o backend Python está rodando (uvicorn main:app).");
        } else {
          alert("Erro desconhecido ao enviar o arquivo.");
        }
      } finally {
        this.loading = false;
      }
    },

    // Lógica de Conversão de Notas
    convertConceptToGrade(concept) {
      const map = {
        'E': 9.5, 'EXCELENTE': 9.5,
        'B': 8.0, 'BOM': 8.0,
        'R': 6.0, 'REGULAR': 6.0,
        'I': 2.5, 'INSUFICIENTE': 2.5
      };
      return map[concept] || 0.0;
    },

    // Adicionar Manualmente
    addManualDiscipline() {
      const novaDisciplina = {
        id_materia: this.manualForm.nome.toUpperCase(), // Usando nome como ID visual
        conceito: this.manualForm.conceito,
        situacao: this.manualForm.situacao,
        nota: this.convertConceptToGrade(this.manualForm.conceito)
      };

      this.parsedData.push(novaDisciplina);
      
      // Reset form
      this.manualForm.nome = '';
      this.manualForm.conceito = 'EXCELENTE';
      this.manualForm.situacao = 'APROVADO';
      
      alert("Disciplina adicionada à lista abaixo! Clique em 'Salvar' para confirmar.");
    },

    updateNotaFromConcept(item) {
      item.nota = this.convertConceptToGrade(item.conceito);
    },

    getConceptColor(concept) {
      if (['E', 'B'].includes(concept)) return 'text-green-600';
      if (concept === 'R') return 'text-yellow-600';
      if (['I', '0', '1'].includes(concept)) return 'text-red-600';
      return 'text-gray-400';
    },

    removeLine(index) {
      this.parsedData.splice(index, 1);
    },

async saveData() {
      if (this.parsedData.length === 0) return;
      
      this.loading = true;

      try {
        const response = await api.post('/api/salvar-historico', this.parsedData);
        console.log('Resposta do Python:', response.data);
        alert(`Sucesso! ${response.data.total_registros} matérias e notas foram salvas.`);
        this.parsedData = [];
        this.$router.push('/dashboard');

      } catch (error) {
        console.error("Erro ao salvar:", error);
        alert("Erro ao salvar os dados. Verifique o console.");
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.custom-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 2px solid #e0e6dc;
  border-radius: 10px;
  font-size: 14px;
  background: #f8f9f7;
  transition: all 0.3s;
  color: #333;
  outline: none;
}

.custom-input:focus {
  border-color: #2c5530;
  background: white;
  box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>