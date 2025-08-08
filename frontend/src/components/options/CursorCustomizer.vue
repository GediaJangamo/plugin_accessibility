<template>
  <div class="p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
    <div class="flex items-center mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-[#3b82f6] dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
      </svg>
      <h3 class="font-medium text-lg text-gray-800 dark:text-white">Cursor</h3>
    </div>
    <p class="text-sm text-[#64748b] dark:text-gray-400 mb-2">Amplie o cursor e altere a sua cor</p>
    <div class="flex gap-3">
      <button 
        @click="setCursorColor('white')"
        class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium text-lg"
        :class="cursorColor === 'white' ? 'ring-2 ring-[#3b82f6] bg-white text-black' : 'bg-white text-black'"
      >
        BRANCO
      </button>
      <button 
        @click="setCursorColor('black')"
        class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium text-lg"
        :class="cursorColor === 'black' ? 'ring-2 ring-[#3b82f6] bg-gray-900 text-white' : 'bg-gray-900 text-white'"
      >
        PRETO
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CursorCustomizer',
  props: {
    cursorColor: {
      type: String,
      default: 'black'
    }
  },
  data() {
    return {
      styleElement: null,
      observer: null,
      cursorInterval: null,
      isUpdating: false
    }
  },
  watch: {
    cursorColor: {
      immediate: true,
      handler(newValue) {
        this.applyCursorColor(newValue);
      }
    }
  },
  mounted() {
    this.addCursorStyles();
    this.startCursorWatcher();
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    setCursorColor(color) {
      this.$emit('update:cursorColor', color);
    },
    
    applyCursorColor(color) {
      if (this.isUpdating) return;
      
      // Remove classes antigas
      document.documentElement.classList.remove('cursor-color-black', 'cursor-color-white');
      document.body.classList.remove('cursor-color-black', 'cursor-color-white');
      
      // Adiciona nova classe
      document.documentElement.classList.add(`cursor-color-${color}`);
      document.body.classList.add(`cursor-color-${color}`);
      
      // Reaplicar estilos
      this.addCursorStyles();
    },
    
    addCursorStyles() {
      if (this.isUpdating) return;
      this.isUpdating = true;
      
      // Remove estilo anterior se existir
      if (this.styleElement) {
        this.styleElement.remove();
      }
      
      // Cria novo elemento de estilo
      this.styleElement = document.createElement('style');
      this.styleElement.innerHTML = `
        /* CURSOR GLOBAL - Versão Otimizada */
        
        /* Cursor branco para todo o sistema */
        html.cursor-color-white,
        html.cursor-color-white body,
        html.cursor-color-white * {
          cursor: url('/static/core/img/cb1.png') 15 15, auto !important;
        }
        
        /* Cursor preto para todo o sistema */
        html.cursor-color-black,
        html.cursor-color-black body,
        html.cursor-color-black * {
          cursor: url('/static/core/img/cn2.png') 15 15, auto !important;
        }
        
        /* Elementos clicáveis - cursor branco */
        html.cursor-color-white a,
        html.cursor-color-white button,
        html.cursor-color-white input[type="button"],
        html.cursor-color-white input[type="submit"],
        html.cursor-color-white [onclick],
        html.cursor-color-white [role="button"] {
          cursor: url('/static/core/img/cb1.png') 15 15, pointer !important;
        }
        
        /* Elementos clicáveis - cursor preto */
        html.cursor-color-black a,
        html.cursor-color-black button,
        html.cursor-color-black input[type="button"],
        html.cursor-color-black input[type="submit"],
        html.cursor-color-black [onclick],
        html.cursor-color-black [role="button"] {
          cursor: url('/static/core/img/cn2.png') 15 15, pointer !important;
        }
        
        /* Campos de texto - cursor branco */
        html.cursor-color-white input[type="text"],
        html.cursor-color-white input[type="email"],
        html.cursor-color-white input[type="password"],
        html.cursor-color-white textarea {
          cursor: url('/static/core/img/cb1.png') 15 15, text !important;
        }
        
        /* Campos de texto - cursor preto */
        html.cursor-color-black input[type="text"],
        html.cursor-color-black input[type="email"],
        html.cursor-color-black input[type="password"],
        html.cursor-color-black textarea {
          cursor: url('/static/core/img/cn2.png') 15 15, text !important;
        }
        
        /* Sobrescreve estilos específicos sem causar conflitos */
        html.cursor-color-white [style*="cursor"]:not([style*="none"]),
        html.cursor-color-black [style*="cursor"]:not([style*="none"]) {
          cursor: inherit !important;
        }
      `;
      
      document.head.appendChild(this.styleElement);
      
      setTimeout(() => {
        this.isUpdating = false;
      }, 100);
    },
    
    startCursorWatcher() {
      // Reaplica o cursor a cada 10 segundos (menos frequente para evitar bugs)
      this.cursorInterval = setInterval(() => {
        if (!this.isUpdating && 
            (document.documentElement.classList.contains('cursor-color-white') || 
             document.documentElement.classList.contains('cursor-color-black'))) {
          this.addCursorStyles();
        }
      }, 10000);
      
      // Observer mais simples para mudanças importantes no DOM
      this.observer = new MutationObserver((mutations) => {
        if (this.isUpdating) return;
        
        let needsUpdate = false;
        
        mutations.forEach(mutation => {
          // Só atualiza se elementos importantes foram adicionados
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            for (let node of mutation.addedNodes) {
              if (node.nodeType === 1 && // Element node
                  (node.tagName === 'MAIN' || 
                   node.tagName === 'SECTION' || 
                   node.id === 'app' || 
                   node.id === 'root' ||
                   node.classList.contains('page') ||
                   node.classList.contains('content'))) {
                needsUpdate = true;
                break;
              }
            }
          }
        });
        
        if (needsUpdate) {
          setTimeout(() => {
            if (!this.isUpdating && 
                (document.documentElement.classList.contains('cursor-color-white') || 
                 document.documentElement.classList.contains('cursor-color-black'))) {
              this.addCursorStyles();
            }
          }, 500);
        }
      });
      
      this.observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    },
    
    cleanup() {
      this.isUpdating = false;
      
      // Limpa o intervalo
      if (this.cursorInterval) {
        clearInterval(this.cursorInterval);
        this.cursorInterval = null;
      }
      
      // Desconecta o observer
      if (this.observer) {
        this.observer.disconnect();
        this.observer = null;
      }
      
      // Remove o estilo
      if (this.styleElement) {
        this.styleElement.remove();
        this.styleElement = null;
      }
      
      // Remove as classes
      document.documentElement.classList.remove('cursor-color-black', 'cursor-color-white');
      document.body.classList.remove('cursor-color-black', 'cursor-color-white');
    }
  }
}
</script>