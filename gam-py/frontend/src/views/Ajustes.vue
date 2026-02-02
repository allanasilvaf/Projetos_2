<template>
  <div class="min-h-screen bg-gray-50 p-6 font-poppins">
    <div class="max-w-6xl mx-auto space-y-8">
      
      <div class="flex items-center justify-between mb-2">
        <div>
          <h1 class="text-2xl font-bold text-dark">Configurações de Perfil</h1>
          <p class="text-gray-500 text-sm">Gerencie seus dados e seu histórico acadêmico.</p>
        </div>
        <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center text-primary font-bold uppercase">
          {{ user.nome ? user.nome.charAt(0) : 'U' }}
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-dark flex items-center gap-2">
            <User :size="20" class="text-primary" /> Dados Pessoais
          </h2>
          <button 
            @click="updateUserProfile" 
            :disabled="loadingUpdate"
            class="px-5 py-2 bg-primary text-white rounded-xl text-sm font-bold hover:bg-green-700 transition flex items-center gap-2 shadow-md"
            :class="{'opacity-70': loadingUpdate}"
          >
            <CheckCircle v-if="!loadingUpdate" :size="16" />
            <Loader2 v-else :size="16" class="animate-spin" />
            {{ loadingUpdate ? 'Salvando...' : 'Confirmar Alterações' }}
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="text-xs font-bold text-gray-500 uppercase mb-1 block">Nome Completo</label>
            <div class="relative">
              <input type="text" v-model="user.nome" class="custom-input pl-12" placeholder="Carregando nome...">
              <User class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-500 uppercase mb-1 block">Curso</label>
            <div class="relative">
              <select v-model="user.curso" class="custom-input pl-12 appearance-none cursor-pointer">
                <option value="" disabled>Selecione seu curso</option>
                <option value="Engenharia de Computação">Engenharia de Computação</option>
                <option value="Engenharia Civil">Engenharia Civil</option>
                <option value="Engenharia Mecânica">Engenharia Mecânica</option>
                <option value="Ciência da Computação">Ciência da Computação</option>
                <option value="Sistemas de Informação">Sistemas de Informação</option>
              </select>
              <BookOpen class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">▼</div>
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-400 uppercase mb-1 block flex items-center gap-1">
              E-mail <Lock :size="12" />
            </label>
            <div class="relative">
              <input type="email" v-model="user.email" class="custom-input-locked pl-12" readonly placeholder="email@exemplo.com">
              <Mail class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-400 uppercase mb-1 block flex items-center gap-1">
              Matrícula <Lock :size="12" />
            </label>
            <div class="relative">
              <input type="text" v-model="user.matricula" class="custom-input-locked pl-12" readonly placeholder="000000000">
              <Hash class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <h2 class="text-lg font-bold text-dark mb-4 flex items-center gap-2">
          <UploadCloud :size="20" class="text-primary" /> Atualizar Histórico (PDF)
        </h2>
        
        <div 
          class="border-2 border-dashed border-gray-300 rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-green-50 hover:border-primary transition-all group relative text-center h-32"
          @dragover.prevent
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <input type="file" ref="fileInput" accept=".pdf" class="hidden" @change="handleFileSelect">
          <UploadCloud :size="28" class="text-gray-400 group-hover:text-primary mb-2 transition-colors" />
          <p class="text-sm font-bold text-gray-600">Clique para enviar novo PDF do SIGAA</p>
          <p class="text-xs text-gray-400">Ou arraste o arquivo aqui</p>
          
          <div v-if="loading" class="absolute inset-0 bg-white/90 flex flex-col items-center justify-center z-10 rounded-2xl">
            <Loader2 :size="30" class="animate-spin text-primary mb-2" />
            <span class="text-xs font-bold text-primary">Processando...</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <div>
            <h2 class="text-lg font-bold text-dark flex items-center gap-2">
              <FileText :size="20" class="text-primary" /> Matérias Cursadas
            </h2>
            <p class="text-xs text-gray-500 mt-1">Total: {{ parsedData.length }} disciplinas registradas</p>
          </div>
          
          <button 
            @click="showManualForm = !showManualForm" 
            class="px-4 py-2 bg-white border border-gray-200 text-primary rounded-lg text-sm font-bold hover:bg-gray-50 flex items-center gap-2 transition-all shadow-sm"
          >
            <PlusCircle :size="16" />
            {{ showManualForm ? 'Fechar Formulário' : 'Adicionar Manualmente' }}
          </button>
        </div>

        <div v-if="showManualForm" class="bg-green-50/50 p-6 border-b border-gray-100 animate-fadeIn">
          <h3 class="text-sm font-bold text-primary mb-4">Adicionar Nova Disciplina</h3>
          <form @submit.prevent="addManualDiscipline" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div class="md:col-span-2">
              <label class="text-[10px] font-bold text-gray-500 uppercase mb-1 block">Nome da Matéria</label>
              <input type="text" v-model="manualForm.nome" placeholder="Ex: Cálculo Numérico" class="custom-input bg-white" required>
            </div>
            <div>
              <label class="text-[10px] font-bold text-gray-500 uppercase mb-1 block">Conceito</label>
              <select v-model="manualForm.conceito" class="custom-input bg-white appearance-none" required>
                <option value="EXCELENTE">Excelente (9.5)</option>
                <option value="BOM">Bom (8.0)</option>
                <option value="REGULAR">Regular (6.0)</option>
                <option value="INSUFICIENTE">Insuficiente (2.5)</option>
              </select>
            </div>
            <button type="submit" class="h-[45px] bg-primary text-white rounded-lg font-bold text-sm hover:bg-green-700 transition flex items-center justify-center gap-2">
              <PlusCircle :size="16" /> Adicionar
            </button>
          </form>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left">
            <thead class="bg-gray-50 text-gray-500 uppercase font-bold text-[11px] border-b border-gray-100">
              <tr>
                <th class="px-6 py-4">Disciplina</th>
                <th class="px-6 py-4">Conceito</th>
                <th class="px-6 py-4">Nota Calc.</th>
                <th class="px-6 py-4">Situação</th>
                <th class="px-6 py-4 text-center">Ações</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="parsedData.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-gray-400 italic">
                  Nenhuma disciplina registrada ainda.
                </td>
              </tr>
              <tr v-for="(item, index) in parsedData" :key="index" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-6 py-4 font-medium text-dark">{{ item.id_materia }}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 rounded text-[10px] font-bold" :class="getBadgeColor(item.conceito)">
                    {{ item.conceito }}
                  </span>
                </td>
                <td class="px-6 py-4 font-mono text-gray-600">{{ item.nota }}</td>
                <td class="px-6 py-4 text-xs font-bold" :class="item.situacao === 'APROVADO' ? 'text-green-600' : 'text-red-500'">
                  {{ item.situacao }}
                </td>
                <td class="px-6 py-4 text-center">
                  <button @click="removeLine(index)" class="p-2 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-full transition-all">
                    <Trash2 :size="16" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="p-4 bg-gray-50 border-t border-gray-200 flex justify-end" v-if="hasUnsavedChanges">
           <button @click="saveData" :disabled="loading" class="px-6 py-3 bg-gradient-to-r from-[#2c5530] to-[#4a7c59] text-white rounded-xl text-sm font-bold hover:shadow-lg transition-all flex items-center gap-2">
             <CheckCircle :size="18" /> Salvar Alterações
           </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { 
  User, Mail, Hash, BookOpen, Lock, CheckCircle, Loader2, 
  UploadCloud, FileText, PlusCircle, Trash2 
} from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'PerfilView',
  components: { 
    User, Mail, Hash, BookOpen, Lock, CheckCircle, Loader2, 
    UploadCloud, FileText, PlusCircle, Trash2 
  },
  data() {
    return {
      loading: false,
      loadingUpdate: false,
      showManualForm: false,
      hasUnsavedChanges: false,
      user: { id: null, nome: '', email: '', matricula: '', curso: '' },
      parsedData: [],
      manualForm: { nome: '', conceito: 'EXCELENTE', situacao: 'APROVADO' }
    }
  },
  async mounted() {
    // === AQUI ESTÁ A CORREÇÃO PRINCIPAL ===
    // Tenta pegar o ID do localStorage (salvo no login)
    // Se não tiver, tenta pegar o objeto 'user' inteiro e extrair o ID
    let savedId = localStorage.getItem('user_id');
    
    if (!savedId) {
       const userStorage = localStorage.getItem('user');
       if (userStorage) {
         try {
           const u = JSON.parse(userStorage);
           savedId = u.id;
         } catch(e) { console.log(e) }
       }
    }

    if (savedId) {
      console.log("ID encontrado no storage:", savedId);
      await this.fetchUserProfile(savedId);
    } else {
      console.warn("Nenhum ID de usuário encontrado. Faça login novamente.");
      // Opcional: Redirecionar para login
      // this.$router.push('/login'); 
    }
    
    await this.fetchUserHistory();
  },
  methods: {
    async fetchUserProfile(id) {
      try {
        const response = await api.get(`/api/usuarios/${id}`);
        this.user = response.data;
        this.user.id = id;
      } catch (error) {
        console.error("Erro ao carregar usuário:", error);
      }
    },
    async updateUserProfile() {
      this.loadingUpdate = true;
      try {
        await api.put(`/api/usuarios/${this.user.id}`, this.user);
        alert("✅ Dados pessoais atualizados!");
      } catch (error) {
        alert("❌ Erro ao atualizar dados.");
      } finally {
        this.loadingUpdate = false;
      }
    },
    async fetchUserHistory() {
      try {
        const response = await api.get('/api/historico');
        this.parsedData = response.data;
      } catch (error) {
        console.error("Erro ao carregar histórico:", error);
      }
    },
    // ... (restante dos métodos iguais: addManualDiscipline, processFile, saveData, etc)
    addManualDiscipline() {
      if (!this.manualForm.nome) return;
      const nova = {
        id_materia: this.manualForm.nome.toUpperCase(),
        conceito: this.manualForm.conceito,
        situacao: 'APROVADO',
        nota: this.convertConceptToGrade(this.manualForm.conceito)
      };
      if (['INSUFICIENTE'].includes(nova.conceito)) nova.situacao = 'REPROVADO';
      this.parsedData.unshift(nova);
      this.manualForm.nome = '';
      this.hasUnsavedChanges = true;
    },
    handleFileSelect(e) { if (e.target.files?.[0]) this.processFile(e.target.files[0]); },
    handleDrop(e) { if (e.dataTransfer.files?.[0]) this.processFile(e.dataTransfer.files[0]); },
    async processFile(file) {
      this.loading = true;
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await api.post('/api/parse-historico', formData);
        const novas = response.data.map(item => ({ ...item, nota: this.convertConceptToGrade(item.conceito) }));
        this.parsedData = [...novas, ...this.parsedData];
        this.hasUnsavedChanges = true;
        alert("PDF lido com sucesso!");
      } catch (error) { alert("Erro ao ler PDF."); } finally { this.loading = false; }
    },
    async saveData() {
      if (!this.parsedData.length) return;
      this.loading = true;
      try {
        await api.post('/api/salvar-historico', this.parsedData);
        alert("✅ Histórico salvo!");
        this.hasUnsavedChanges = false;
      } catch (e) { alert("Erro ao salvar."); } finally { this.loading = false; }
    },
    removeLine(index) {
      if(confirm("Remover disciplina?")) { this.parsedData.splice(index, 1); this.hasUnsavedChanges = true; }
    },
    convertConceptToGrade(c) {
      const map = { 'E': 9.5, 'EXCELENTE': 9.5, 'B': 8.0, 'BOM': 8.0, 'R': 6.0, 'REGULAR': 6.0, 'I': 2.5, 'INSUFICIENTE': 2.5 };
      return map[c] || 0.0;
    },
    getBadgeColor(c) {
      if (['EXCELENTE', 'E', 'BOM', 'B'].includes(c)) return 'bg-green-100 text-green-700';
      if (['REGULAR', 'R'].includes(c)) return 'bg-yellow-100 text-yellow-700';
      return 'bg-red-100 text-red-700';
    }
  }
}
</script>

<style scoped>
/* A CORREÇÃO DE LAYOUT ESTÁ AQUI: padding-left: 45px */
.custom-input, .custom-input-locked {
  width: 100%;
  padding: 12px 12px 12px 45px !important; /* Espaço para o ícone */
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.custom-input { background: white; color: #1f2937; }
.custom-input:focus { border-color: #2c5530; box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1); }

.custom-input-locked {
  background: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fadeIn { animation: fadeIn 0.3s ease-out; }
.text-primary { color: #2c5530; }
.bg-primary { background-color: #2c5530; }
</style>