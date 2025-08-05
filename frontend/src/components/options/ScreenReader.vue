<template>
  <div class="p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
    <label class="flex items-center cursor-pointer">
      <div class="flex-shrink-0 mr-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-[#3b82f6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </div>
      <div class="flex-grow">
        <span class="block text-lg text-gray-800 dark:text-white font-medium">Leitor de ecrã</span>
        <span class="text-sm text-[#64748b] dark:text-gray-300">Narração de conteúdos</span>
      </div>
      <div class="flex items-center">
        <input
           type="checkbox"
           id="screen-reader"
           :checked="screenReader"
           @change="toggleScreenReader"
           class="sr-only"
        >
        <div class="relative w-14 h-7 bg-gray-300  dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-blue-400': screenReader}">
          <div class="absolute left-1 top-1 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-7': screenReader}"></div>
        </div>
      </div>
    </label>
    
    <!-- Teleport para colocar o controle do leitor de tela no final do body -->
    <teleport to="body">
      <ScreenReaderControl :active="screenReader" />
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
      this.$emit('announce', newValue ? 'Leitor de ecra activado' : 'Leitor de ecra desactivado');
      
      // Adicionar classes de estilo global para o leitor de tela
      if (newValue) {
        this.addScreenReaderStyles();
      } else {
        this.removeScreenReaderStyles();
      }
    },
    
    addScreenReaderStyles() {
      const styleEl = document.createElement('style');
      styleEl.id = 'screen-reader-styles';
      styleEl.innerHTML = `
        .reading-highlight {
          outline: 2px solid #077b4b !important;
          box-shadow: 0 0 5px rgba(7, 123, 75, 0.5) !important;
          transition: outline 0.3s ease, box-shadow 0.3s ease !important;
        }
      `;
      document.head.appendChild(styleEl);
    },
    
    removeScreenReaderStyles() {
      const styleEl = document.getElementById('screen-reader-styles');
      if (styleEl) {
        document.head.removeChild(styleEl);
      }
      
      // Remove qualquer destaque existente
      document.querySelectorAll('.reading-highlight').forEach(el => {
        el.classList.remove('reading-highlight');
        el.style.outline = '';
      });
    }
  },
  beforeUnmount() {
    this.removeScreenReaderStyles();
  }
}
</script>