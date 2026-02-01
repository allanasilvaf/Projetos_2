<template>
  <div class="max-w-4xl mx-auto py-10 px-6">
    
    <h1 class="text-3xl font-bold text-dark mb-8 flex items-center gap-3">
      <Settings :size="32" class="text-primary" />
      Ajustes & Importação
    </h1>

    <div class="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden">
      
      <div class="p-8 border-b border-gray-100">
        <h2 class="text-xl font-bold text-dark mb-2">Histórico UFPA (Conceitos)</h2>
        <p class="text-gray-500 text-sm">
          Envie seu PDF do SIGAA. O sistema identificará as matérias pelo código (ID). Verifique se os conceitos (E, B, R, I) estão corretos.
        </p>
      </div>

      <div v-if="!parsedData.length" class="p-8">
        <div 
          class="border-2 border-dashed border-gray-300 rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer hover:bg-green-50 hover:border-primary transition-all group relative"
          @dragover.prevent
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <input type="file" ref="fileInput" accept=".pdf" class="hidden" @change="handleFileSelect">
          
          <div class="w-16 h-16 bg-green-100 text-primary rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <UploadCloud :size="32" />
          </div>
          
          <h3 class="font-bold text-dark text-lg mb-1">Clique ou arraste seu PDF aqui</h3>
          <p class="text-gray-400 text-sm">Suportamos apenas arquivos .PDF oficiais do SIGAA</p>
          
          <div v-if="loading" class="absolute inset-0 bg-white/90 flex flex-col items-center justify-center z-10 rounded-2xl">
            <Loader2 :size="40" class="animate-spin text-primary mb-2" />
            <span class="text-primary font-bold">Processando histórico...</span>
          </div>
        </div>
      </div>

      <div v-else class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg text-dark">Conferência Rápida</h3>
          <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded border border-gray-200">
            Legenda: E (Excelente) | B (Bom) | R (Regular) | I (Insuficiente)
          </span>
        </div>

        <div class="overflow-x-auto border border-gray-200 rounded-xl mb-6 max-h-[400px] overflow-y-auto custom-scrollbar">
          <table class="w-full text-sm text-left">
            <thead class="bg-gray-50 text-gray-500 uppercase font-bold text-xs sticky top-0 z-10 shadow-sm">
              <tr>
                <th class="px-4 py-3 bg-gray-50">ID Matéria</th>
                <th class="px-4 py-3 bg-gray-50">Conceito</th>
                <th class="px-4 py-3 bg-gray-50">Situação</th>
                <th class="px-4 py-3 bg-gray-50 text-center">Remover</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="(item, index) in parsedData" :key="index" class="hover:bg-gray-50 transition-colors">
                
                <td class="px-4 py-2 font-mono font-bold text-primary">
                  {{ item.id_materia }}
                </td>

                <td class="px-4 py-2">
                  <select 
                    v-if="item.situacao !== 'MATRICULADO' && item.situacao !== 'TRANCADO'"
                    v-model="item.conceito"
                    class="bg-white border border-gray-300 rounded px-2 py-1 font-bold focus:border-primary outline-none cursor-pointer w-32"
                    :class="{
                      'text-green-600': ['E', 'B'].includes(item.conceito),
                      'text-yellow-600': item.conceito === 'R',
                      'text-red-600': ['I', '1', '0'].includes(item.conceito)
                    }"
                  >
                    <option value="E">E (Excelente)</option>
                    <option value="B">B (Bom)</option>
                    <option value="R">R (Regular)</option>
                    <option value="I">I (Insuficiente)</option>
                    <option value="S">S (Sem Conceito)</option>
                  </select>
                  <span v-else class="text-gray-400 italic text-xs pl-2">
                    {{ item.situacao === 'TRANCADO' ? 'Trancado' : 'Cursando...' }}
                  </span>
                </td>

                <td class="px-4 py-2">
                  <span 
                    class="px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide"
                    :class="{
                      'bg-green-100 text-green-700': item.situacao.includes('APROVADO'),
                      'bg-red-100 text-red-700': item.situacao.includes('REPROVADO'),
                      'bg-blue-100 text-blue-700': item.situacao.includes('MATRICULADO'),
                      'bg-gray-100 text-gray-600': ['TRANCADO', 'CANCELADO'].some(s => item.situacao.includes(s))
                    }"
                  >
                    {{ item.situacao }}
                  </span>
                </td>

                <td class="px-4 py-2 text-center">
                  <button @click="removeLine(index)" class="text-gray-300 hover:text-red-500 transition-colors p-1 rounded-full hover:bg-red-50">
                    <Trash2 :size="16" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex justify-end gap-3 border-t pt-4 border-gray-100">
          <button @click="parsedData = []" class="px-6 py-2 rounded-full text-gray-500 font-bold hover:bg-gray-50 transition-colors border border-transparent hover:border-gray-200">
            Cancelar
          </button>
          <button @click="saveData" class="px-6 py-2 rounded-full bg-primary text-white font-bold hover:bg-green-700 shadow-md flex items-center gap-2 transform active:scale-95 transition-all">
            <CheckCircle :size="18" />
            Salvar no Perfil
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { Settings, UploadCloud, Loader2, Trash2, CheckCircle } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'AjustesView',
  components: { Settings, UploadCloud, Loader2, Trash2, CheckCircle },
  data() {
    return {
      loading: false,
      parsedData: []
    }
  },
  methods: {
    // 1. Seleção via Clique
    handleFileSelect(e) {
      if (e.target.files && e.target.files[0]) {
        this.processFile(e.target.files[0]);
      }
    },
    
    // 2. Seleção via Arrastar (Adicionei este método que faltava)
    handleDrop(e) {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.processFile(e.dataTransfer.files[0]);
      }
    },

    async processFile(file) {
      this.loading = true;

      // Validação básica de extensão
      if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) {
         alert('Por favor, envie apenas arquivos PDF.');
         this.loading = false;
         return;
      }

      const formData = new FormData();
      formData.append('file', file); 

      try {
        // Integração com Backend Python
        const response = await api.post('/api/parse-historico', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.parsedData = response.data;
        
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

    removeLine(index) {
      this.parsedData.splice(index, 1);
    },

async saveData() {
      // Se a lista estiver vazia, não faz nada
      if (this.parsedData.length === 0) return;
      
      this.loading = true; // Mostra um loading (opcional, se quiser criar estado visual)

      try {
        // Envia o JSON limpo para o Python
        // O Axios converte automaticamente o array parsedData para JSON
        const response = await api.post('/api/salvar-historico', this.parsedData);
        
        console.log('Resposta do Python:', response.data);
        
        // Sucesso!
        alert(`Sucesso! ${response.data.total_registros} matérias foram salvas no seu perfil.`);
        
        // Limpa a tela ou redireciona para o Dashboard
        this.parsedData = [];
        this.$router.push('/dashboard'); // Descomente se quiser mandar o usuário pro Dashboard

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
/* Scrollbar fina para a tabela */
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