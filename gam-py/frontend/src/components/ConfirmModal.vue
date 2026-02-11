<template>
  <Transition name="fade">
    <div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div class="bg-white rounded-3xl shadow-2xl max-w-sm w-full p-8 transform transition-all animate-popIn">
        <div class="flex flex-col items-center text-center">
          <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center text-red-500 mb-4">
            <LogOut :size="32" />
          </div>
          
          <h3 class="text-xl font-bold text-dark mb-2">{{ title }}</h3>
          <p class="text-gray-500 text-sm mb-8">{{ message }}</p>
          
          <div class="flex gap-3 w-full">
            <button 
              @click="$emit('cancel')" 
              class="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-2xl font-bold text-sm transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="$emit('confirm')" 
              class="flex-1 px-4 py-3 bg-red-500 hover:bg-red-600 text-white rounded-2xl font-bold text-sm shadow-lg shadow-red-200 transition-colors"
            >
              Sim
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { LogOut } from 'lucide-vue-next';
defineProps(['show', 'title', 'message']);
defineEmits(['confirm', 'cancel']);
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@keyframes popIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-popIn { animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
</style>