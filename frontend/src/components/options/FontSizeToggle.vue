<!-- FontSizeToggle -->
<template>
  <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
    <h3 class="font-medium text-lg text-gray-800 dark:text-gray-200 mb-3 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
      </svg>
      Tamanho da Fonte
    </h3>
    <div class="flex items-center justify-between">
      <button 
        @click="decreaseFont" 
        class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-6 py-2 rounded-lg font-bold text-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        aria-label="Diminuir fonte"
      >
        A-
      </button>
      <div class="text-center">
        <span class="text-base text-gray-600 dark:text-gray-300 block">Tamanho</span>
        <span class="font-medium text-lg text-gray-800 dark:text-white">{{ fontSize }}</span>
      </div>
      <button 
        @click="increaseFont" 
        class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-6 py-2 rounded-lg font-bold text-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        aria-label="Aumentar fonte"
      >
        A+
      </button>
    </div>
  </div>
</template>

<script>
// Em FontSizeToggle.vue
export default {
  name: 'FontSizeToggle',
  props: {
    fontSize: {
      type: String,
      default: 'Normal'
    }
  },
  watch: {
    fontSize: {
      immediate: true,
      handler(newValue) {
        this.applyFontSize(newValue);
      }
    }
  },
  methods: {
    increaseFont() {
      // Usar uma abordagem que funcione sem depender de 'main-content'
      // Selecionar o elemento principal do conteúdo, excluindo o menu de acessibilidade
      const contentElements = document.querySelectorAll('main, #app > div:not([role="dialog"])');
      
      contentElements.forEach(element => {
        // Pegar o tamanho atual da fonte
        const currentSize = window.getComputedStyle(element).fontSize;
        // Aumentar em 10%
        const newSize = parseFloat(currentSize) * 1.1;
        element.style.fontSize = `${newSize}px`;
      });
      
      this.$emit('update:fontSize', 'Grande');
      this.$emit('announce', 'Tamanho da fonte aumentado');
    },
    
    decreaseFont() {
      // Usar a mesma abordagem para diminuir a fonte
      const contentElements = document.querySelectorAll('main, #app > div:not([role="dialog"])');
      
      contentElements.forEach(element => {
        const currentSize = window.getComputedStyle(element).fontSize;
        const newSize = parseFloat(currentSize) * 0.9;
        element.style.fontSize = `${newSize}px`;
      });
      
      this.$emit('update:fontSize', 'Pequeno');
      this.$emit('announce', 'Tamanho da fonte diminuído');
    },
    
    applyFontSize(size) {
      // Aplicar o tamanho de fonte ao conteúdo principal
      const contentElements = document.querySelectorAll('main, #app > div:not([role="dialog"])');
      
      if (size === 'Normal') {
        contentElements.forEach(element => {
          element.style.fontSize = '';
        });
      } else {
        const defaultSize = '16px';
        const factor = size === 'Grande' ? 1.1 : 0.9;
        
        contentElements.forEach(element => {
          element.style.fontSize = `${parseFloat(defaultSize) * factor}px`;
        });
      }
    }
  }
}
</script>