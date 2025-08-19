<template>
  <div class="p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300 mx-2 sm:mx-0">
    <label class="flex items-center cursor-pointer">
      <div class="flex-shrink-0 mr-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#3b82f6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </div>
      <div class="flex-grow overflow-hidden">
        <span class="block text-base text-gray-800 dark:text-white font-medium truncate">Leitor de ecrã</span>
        <span class="text-xs text-[#64748b] dark:text-gray-300 truncate">Narração de conteúdos</span>
      </div>
      <div class="flex items-center ml-2">
        <input 
          type="checkbox"
          id="screen-reader"
          :checked="screenReader"
          @change="toggleScreenReader"
          class="sr-only"
        >
        <div class="relative w-12 h-6 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-blue-500': screenReader}">
          <div class="absolute left-0.5 top-0.5 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-6': screenReader}"></div>
        </div>
      </div>
    </label>
         
    <!-- Teleport para colocar o controle do leitor de tela no final do body -->
    <teleport to="body">
      <div class="fixed inset-0 z-50 flex items-end justify-center" v-if="screenReader">
        <div class="bg-white dark:bg-gray-800 rounded-t-lg shadow-xl w-full max-w-md mx-2 sm:mx-auto mb-2 overflow-hidden">
          <div class="flex justify-between items-center p-4 border-b dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Controlo do Leitor</h3>
            <button 
              @click="toggleScreenReader"
              class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none"
              aria-label="Fechar leitor de ecrã"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="p-4">
            <ScreenReaderControl :active="screenReader" @update:screenReader="updateScreenReader" />
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script>
import ScreenReaderControl from '../controller/ScreenReaderControl.vue';

export default {
  name: 'ScreenReader',
  components: {
    ScreenReaderControl
  },
  props: {
    screenReader: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    toggleScreenReader() {
      const newValue = !this.screenReader;
      this.$emit('update:screenReader', newValue);
      this.$emit('announce', newValue ? 'Leitor de ecrã activado' : 'Leitor de ecrã desactivado');
    },
    
    updateScreenReader(value) {
      this.$emit('update:screenReader', value);
    }
  }
}
</script>

<style scoped>
/* Estilos personalizados para o toggle */

/* Animação suave para o switch */
input:checked + div {
  background: linear-gradient(135deg, #3b82f6);
}

input:checked + div > div {
  box-shadow: 0 3px 8px #3b82f6;
}
</style>