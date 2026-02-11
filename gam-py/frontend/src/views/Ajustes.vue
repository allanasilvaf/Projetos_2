<template>
  <div class="min-h-screen bg-gray-50 p-6 font-poppins">
    <div class="max-w-6xl mx-auto space-y-8">
      
      <div class="flex items-center justify-between mb-2">
        <div>
          <h1 class="text-2xl font-bold text-dark">
            Seja bem-vindo, {{ user.nome ? user.nome.split(' ')[0] : 'Estudante' }}!
          </h1>
          <p class="text-gray-500 text-sm">Visualize seus dados cadastrais e histórico.</p>
        </div>
        <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center text-primary font-bold uppercase">
          {{ user.nome ? user.nome.charAt(0) : 'U' }}
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <h2 class="text-lg font-bold text-dark mb-6 flex items-center gap-2">
          <User :size="20" class="text-primary" /> Dados Pessoais
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">Nome Completo</label>
            <div class="relative">
              <input type="text" v-model="user.nome" class="custom-input-locked pl-12" readonly>
              <User class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">Curso</label>
            <div class="relative">
              <input type="text" value="Engenharia de Computação" class="custom-input-locked pl-12" readonly>
              <BookOpen class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-400 uppercase mb-1 block">E-mail</label>
            <div class="relative">
              <input type="email" v-model="user.email" class="custom-input-locked pl-12" readonly>
              <Mail class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label class="text-xs font-bold text-gray-500 uppercase mb-1 block">Semestre Atual</label>
            <div class="relative">
              <select v-model="user.semestre" class="custom-input pl-12 appearance-none bg-white cursor-pointer hover:border-primary transition-colors">
                <option value="" disabled>Selecione seu semestre</option>
                <option v-for="n in 10" :key="n" :value="n + 'º Semestre'">{{ n }}º Semestre</option>
              </select>
              <Calendar class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 text-xs">▼</div>
            </div>
          </div>

          <div class="md:col-span-2 flex justify-end">
            <button @click="saveGeneralData" :disabled="loadingGeneral" class="px-6 py-2 bg-primary text-white rounded-xl font-bold text-sm hover:shadow-lg transition-all flex items-center gap-2">
              <Loader2 v-if="loadingGeneral" class="animate-spin" :size="16" />
              <CheckCircle v-else :size="16" />
              Salvar Dados Pessoais
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <h2 class="text-lg font-bold text-dark mb-4 flex items-center gap-2">
          <UploadCloud :size="20" class="text-primary" /> Atualizar Histórico (PDF)
        </h2>
        <div class="border-2 border-dashed border-gray-300 rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-green-50 hover:border-primary transition-all relative h-32" @click="$refs.fileInput.click()">
          <input type="file" ref="fileInput" accept=".pdf" class="hidden" @change="handleFileSelect">
          <UploadCloud :size="28" class="text-gray-400 mb-2" />
          <p class="text-sm font-bold text-gray-600">Clique para enviar novo PDF do SIGAA</p>
          <div v-if="loading" class="absolute inset-0 bg-white/90 flex items-center justify-center z-10 rounded-2xl">
            <Loader2 :size="30" class="animate-spin text-primary" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <div>
            <h2 class="text-lg font-bold text-dark flex items-center gap-2"><FileText :size="20" class="text-primary" /> Matérias Cursadas</h2>
            <p class="text-xs text-gray-500 mt-1">Total: {{ parsedData.length }} disciplinas</p>
          </div>
          <button @click="showManualForm = !showManualForm" class="px-4 py-2 bg-white border border-gray-200 text-primary rounded-lg text-sm font-bold flex items-center gap-2 shadow-sm">
            <PlusCircle :size="16" /> {{ showManualForm ? 'Fechar' : 'Adicionar' }}
          </button>
        </div>

        <div v-if="showManualForm" class="bg-green-50/50 p-6 border-b border-gray-100 animate-fadeIn">
          <form @submit.prevent="addManualDiscipline" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div class="md:col-span-2">
              <label class="text-[10px] font-bold text-gray-500 uppercase mb-1 block">Nome da Matéria</label>
              <input type="text" v-model="manualForm.nome" class="custom-input bg-white" required>
            </div>
            <div>
              <label class="text-[10px] font-bold text-gray-500 uppercase mb-1 block">Conceito</label>
              <select v-model="manualForm.conceito" class="custom-input bg-white" required>
                <option value="EXCELENTE">Excelente</option>
                <option value="BOM">Bom</option>
                <option value="REGULAR">Regular</option>
                <option value="INSUFICIENTE">Insuficiente</option>
              </select>
            </div>
            <button type="submit" class="h-[45px] bg-primary text-white rounded-lg font-bold text-sm hover:bg-green-700 transition">Adicionar</button>
          </form>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left">
            <thead class="bg-gray-50 text-gray-500 uppercase font-bold text-[11px]">
              <tr><th class="px-6 py-4">Disciplina</th><th class="px-6 py-4">Conceito</th><th class="px-6 py-4 text-center">Ações</th></tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="(item, index) in parsedData" :key="index" class="hover:bg-gray-50/50">
                <td class="px-6 py-4 font-medium text-dark">{{ item.id_materia }}</td>
                <td class="px-6 py-4"><span class="px-2 py-1 rounded text-[10px] font-bold" :class="getBadgeColor(item.conceito)">{{ item.conceito }}</span></td>
                <td class="px-6 py-4 text-center"><button @click="removeLine(index)" class="text-gray-300 hover:text-red-500"><Trash2 :size="16"/></button></td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="p-4 bg-gray-50 border-t border-gray-200 flex justify-end" v-if="hasUnsavedChanges">
           <button @click="openSaveHistoryModal" :disabled="loading" class="px-6 py-3 bg-primary text-white rounded-xl font-bold flex items-center gap-2 shadow-lg">
             <CheckCircle :size="18" /> Salvar Histórico
           </button>
        </div>
      </div>

      <div class="flex justify-center pt-4 pb-8">
        <button @click="logout" class="px-8 py-3 bg-red-50 text-red-600 border border-red-200 rounded-xl font-bold flex items-center gap-2">
          <LogOut :size="18" /> Sair
        </button>
      </div>

      <ConfirmModal 
        :show="showSaveConfirmModal" 
        title="Confirmar Registro" 
        message="Deseja salvar as alterações no seu histórico acadêmico?"
        @confirm="executeSaveHistory"
        @cancel="showSaveConfirmModal = false"
      />

      <ConfirmModal 
        :show="showLogoutModal" 
        title="Encerrar Sessão" 
        message="Tem certeza que deseja sair?"
        @confirm="executeLogout"
        @cancel="showLogoutModal = false"
      />

      <Transition name="fade">
        <div v-if="showSuccessPopup" class="fixed bottom-10 right-10 z-[100] bg-white border-l-4 border-green-500 shadow-2xl rounded-2xl p-5 flex items-center gap-4 animate-slideIn">
          <div class="bg-green-100 text-green-600 p-2 rounded-full"><CheckCircle :size="24" /></div>
          <div><p class="font-bold text-dark text-sm">Sucesso!</p><p class="text-gray-500 text-xs">As informações foram salvas no banco.</p></div>
        </div>
      </Transition>

      <Transition name="fade">
        <div v-if="showErrorPopup" class="fixed bottom-10 right-10 z-[100] bg-white border-l-4 border-red-500 shadow-2xl rounded-2xl p-5 flex items-center gap-4 animate-slideIn">
          <div class="bg-red-100 text-red-600 p-2 rounded-full"><XCircle :size="24" /></div>
          <div><p class="font-bold text-dark text-sm">Erro ao Salvar</p><p class="text-gray-500 text-xs">{{ errorMessage }}</p></div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import { User, Mail, Calendar, BookOpen, Lock, CheckCircle, Loader2, UploadCloud, FileText, PlusCircle, Trash2, LogOut, XCircle } from 'lucide-vue-next';
import api from '@/services/api';
import ConfirmModal from '@/components/ConfirmModal.vue';

export default {
  name: 'Ajustes',
  components: { User, Mail, Calendar, BookOpen, Lock, CheckCircle, Loader2, UploadCloud, FileText, PlusCircle, Trash2, LogOut, ConfirmModal, XCircle },
  data() {
    return {
      loading: false,
      loadingGeneral: false,
      showSuccessPopup: false,
      showErrorPopup: false,
      errorMessage: 'O servidor não conseguiu processar os dados.',
      showLogoutModal: false,
      showSaveConfirmModal: false,
      showManualForm: false,
      hasUnsavedChanges: false,
      user: { id: null, nome: '', email: '', semestre: '', curso: 'Engenharia de Computação' },
      parsedData: [],
      manualForm: { nome: '', conceito: 'EXCELENTE' }
    }
  },
  async mounted() {
    const userStorage = localStorage.getItem('user');
    if (userStorage) {
      this.user = { ...this.user, ...JSON.parse(userStorage) };
      this.user.curso = 'Engenharia de Computação';
    } else {
      this.$router.push('/login');
      return;
    }
    if (this.user.id) {
      await this.fetchLatestUserData(this.user.id);
      await this.fetchUserHistory();
    }
  },
  methods: {
    triggerError(msg) {
      this.errorMessage = msg || 'O servidor não conseguiu processar os dados.';
      this.showErrorPopup = true;
      setTimeout(() => { this.showErrorPopup = false; }, 4000);
    },
    async saveGeneralData() {
      this.loadingGeneral = true;
      try {
        const response = await api.put(`/api/ajustes.php/${this.user.id}`, { semestre: this.user.semestre });
        if (response.data.success) {
          localStorage.setItem('user', JSON.stringify(this.user));
          this.showSuccessPopup = true;
          setTimeout(() => { this.showSuccessPopup = false; }, 3000);
        } else {
          this.triggerError(response.data.message);
        }
      } catch (error) {
        this.triggerError("Erro na comunicação com o servidor.");
      } finally {
        this.loadingGeneral = false;
      }
    },
    openSaveHistoryModal() {
      this.showSaveConfirmModal = true;
    },
    async executeSaveHistory() {
      this.showSaveConfirmModal = false;
      this.loading = true;
      try {
        const response = await api.post('/api/salvar-historico.php', this.parsedData);
        if (response.data.success) {
          this.hasUnsavedChanges = false; // Botão some aqui
          this.showSuccessPopup = true;
          setTimeout(() => { this.showSuccessPopup = false; }, 3000);
        } else {
          this.triggerError(response.data.message);
        }
      } catch (e) {
        this.triggerError("Erro ao salvar histórico."); // Removido o alert nativo
      } finally {
        this.loading = false;
      }
    },
    async fetchLatestUserData(id) {
      try {
        const response = await api.get(`/api/ajustes.php/${id}`);
        if (response.data) {
          this.user = { ...this.user, ...response.data };
          this.user.curso = 'Engenharia de Computação';
          localStorage.setItem('user', JSON.stringify(this.user));
        }
      } catch (e) { console.warn("Modo Offline"); }
    },
    async fetchUserHistory() {
      try {
        const response = await api.get('/api/historico.php');
        this.parsedData = response.data;
      } catch (e) { console.error(e); }
    },
    addManualDiscipline() {
      if (!this.manualForm.nome) return;
      this.parsedData.unshift({ id_materia: this.manualForm.nome.toUpperCase(), conceito: this.manualForm.conceito });
      this.hasUnsavedChanges = true; // Botão aparece aqui
      this.manualForm.nome = '';
    },
    logout() { this.showLogoutModal = true; },
    executeLogout() {
      localStorage.clear();
      this.$router.push('/login');
    },
    getBadgeColor(c) {
      if (['EXCELENTE', 'BOM'].includes(c)) return 'bg-green-100 text-green-700';
      return c === 'REGULAR' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700';
    },
    removeLine(i) { 
      this.parsedData.splice(i, 1); 
      this.hasUnsavedChanges = true; // Botão aparece aqui também se deletar algo
    },
    handleFileSelect(e) { /* Lógica de PDF que ativa hasUnsavedChanges */ }
  }
}
</script>

<style scoped>
.custom-input, .custom-input-locked {
  width: 100%;
  padding: 12px 12px 12px 45px !important;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}
.custom-input { background: white; color: #1f2937; }
.custom-input:focus { border-color: #2c5530; box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1); }
.custom-input-locked { background: #f9fafb; color: #6b7280; cursor: default; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.animate-slideIn { animation: slideIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.text-primary { color: #2c5530; }
.bg-primary { background-color: #2c5530; }
</style>