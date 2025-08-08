<!-- FontSizeToggle -->
<template>
  <div class="p-2 bg-[#f1f5f9] dark:bg-gray-800 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow duration-300">
    <!-- Header Section -->
    <div class="flex items-start gap-3 mb-4">
      <!-- <div class="flex-shrink-0 w-10 h-10 bg-[#3b82f6] rounded-lg flex items-center justify-center"> -->
        <svg xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-5 w-5 text-[#3b82f6]">
          <polyline points="4 7 4 4 20 4 20 7" />
          <line x1="9" y1="20" x2="15" y2="20" />
          <line x1="12" y1="4" x2="12" y2="20" />
        </svg>
      <!-- </div> -->
      
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-lg text-gray-900 dark:text-gray-100 leading-tight">
          Tamanho da Fonte
        </h3>
      </div>
    </div>
    
    <!-- Controls Section -->
    <div class="flex items-center justify-between gap-4">
      <button 
        @click="decreaseFont"
        class="flex-shrink-0 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-4 py-3 rounded-lg font-bold text-xl shadow-sm border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
        aria-label="Diminuir tamanho da fonte"
      >
        A-
      </button>
      
      <div class="flex-1 text-center px-2">
        <div class="bg-white dark:bg-gray-700 rounded-lg py-2 px-3 border border-gray-200 dark:border-gray-600">
          <span class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide block mb-1">
            Actual
          </span>
          <!-- <span class="font-semibold text-base text-gray-900 dark:text-white block">
            {{ fontSize }}
          </span> -->
          <span class="font-semibold text-base text-gray-900 dark:text-white block whitespace-nowrap">
            {{ fontSize }}
          </span>

        </div>
      </div>
      
      <button 
        @click="increaseFont"
        class="flex-shrink-0 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-4 py-3 rounded-lg font-bold text-xl shadow-sm border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
        aria-label="Aumentar tamanho da fonte"
      >
        A+
      </button>
    </div>
    
    <!-- Size Indicator (opcional) -->
    <div class="mt-3 flex justify-center">
      <div class="flex gap-1">
        <div 
          v-for="(size) in fontSizes" 
          :key="size"
          class="w-2 h-2 rounded-full transition-colors duration-200"
          :class="fontSize === size ? 'bg-[#3b82f6]' : 'bg-gray-300 dark:bg-gray-600'"
          :aria-label="`${size} - ${fontSize === size ? 'Selecionado' : 'Não selecionado'}`"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FontSizeToggle',
  props: {
    fontSize: {
      type: String,
      default: 'Normal'
    }
  },
  data() {
    return {
      fontSizes: ['Pequeno', 'Normal', 'Grande', 'Muito Grande']
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
      const currentIndex = this.fontSizes.indexOf(this.fontSize);
      const nextIndex = Math.min(currentIndex + 1, this.fontSizes.length - 1);
      const newSize = this.fontSizes[nextIndex];
      
      if (newSize !== this.fontSize) {
        this.$emit('update:fontSize', newSize);
        this.$emit('announce', `Tamanho da fonte alterado para ${newSize}`);
      } else {
        this.$emit('announce', 'Tamanho máximo da fonte já selecionado');
      }
    },
    
    decreaseFont() {
      const currentIndex = this.fontSizes.indexOf(this.fontSize);
      const prevIndex = Math.max(currentIndex - 1, 0);
      const newSize = this.fontSizes[prevIndex];
      
      if (newSize !== this.fontSize) {
        this.$emit('update:fontSize', newSize);
        this.$emit('announce', `Tamanho da fonte alterado para ${newSize}`);
      } else {
        this.$emit('announce', 'Tamanho mínimo da fonte já selecionado');
      }
    },
    
    applyFontSize(size) {
      // Mapeamento mais preciso dos tamanhos
      const fontSizeMap = {
        'Pequeno': '0.875rem',      // 14px
        'Normal': '1rem',           // 16px
        'Grande': '1.125rem',       // 18px
        'Muito Grande': '1.25rem'   // 20px
      };
      
      const fontSize = fontSizeMap[size] || fontSizeMap['Normal'];
      
      // Aplicar ao conteúdo principal, excluindo o menu de acessibilidade
      const contentElements = document.querySelectorAll('main, #app > div:not([role="dialog"]), .main-content, #main-content');
      
      contentElements.forEach(element => {
        if (element && !element.closest('[role="dialog"]')) {
          element.style.fontSize = fontSize;
        }
      });
      
      // Aplicar também ao body como fallback, mas com prioridade menor
      document.body.style.setProperty('--font-size-base', fontSize);
    }
  }
}
</script>

<style scoped>
/* Animações suaves para as transições */
.transition-colors {
  transition-property: color, background-color, border-color;
}

/* Melhor contraste para o modo escuro */
.dark .bg-white {
  background-color: rgb(55 65 81);
}

.dark .border-gray-200 {
  border-color: rgb(75 85 99);
}
</style>