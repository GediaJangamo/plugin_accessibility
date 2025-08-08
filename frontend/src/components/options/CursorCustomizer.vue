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
    // Verifica se há uma preferência salva ao montar o componente
    const savedColor = this.loadCursorPreference();
    if (savedColor && savedColor !== this.cursorColor) {
      this.$emit('update:cursorColor', savedColor);
    }
    
    this.addCursorStyles();
    this.startCursorWatcher();
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    setCursorColor(color) {
      this.$emit('update:cursorColor', color);
      this.saveCursorPreference();
    },
    
    saveCursorPreference() {
      // Salva a preferência no localStorage para persistir entre navegações
      try {
        localStorage.setItem('customCursorColor', this.cursorColor);
        localStorage.setItem('customCursorActive', 'true');
      } catch (e) {
        // Fallback se localStorage não estiver disponível
        window.customCursorSettings = {
          color: this.cursorColor,
          active: true
        };
      }
    },
    
    loadCursorPreference() {
      try {
        const savedColor = localStorage.getItem('customCursorColor');
        const isActive = localStorage.getItem('customCursorActive') === 'true';
        if (savedColor && isActive) {
          return savedColor;
        }
      } catch (e) {
        // Fallback para window object
        if (window.customCursorSettings && window.customCursorSettings.active) {
          return window.customCursorSettings.color;
        }
      }
      return null;
    },
    
    ensureCursorActive() {
      if (this.isUpdating) return;
      
      const hasClass = document.documentElement.classList.contains('cursor-color-white') || 
                       document.documentElement.classList.contains('cursor-color-black');
      
      if (!hasClass) {
        // Reaplica a cor salva
        const savedColor = this.loadCursorPreference();
        if (savedColor) {
          document.documentElement.classList.add(`cursor-color-${savedColor}`);
          document.body.classList.add(`cursor-color-${savedColor}`);
        } else {
          // Aplica a cor atual do prop
          document.documentElement.classList.add(`cursor-color-${this.cursorColor}`);
          document.body.classList.add(`cursor-color-${this.cursorColor}`);
        }
      }
      
      // Sempre reaplica os estilos para garantir que funcionem
      this.addCursorStyles();
    },
    
    handleNavigation() {
      // Callback para mudanças de navegação
      setTimeout(() => {
        this.ensureCursorActive();
      }, 300);
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
      // Salva a escolha do cursor no localStorage para persistir
      this.saveCursorPreference();
      
      // Reaplica o cursor a cada 5 segundos para garantir persistência
      this.cursorInterval = setInterval(() => {
        if (!this.isUpdating) {
          this.ensureCursorActive();
        }
      }, 5000);
      
      // Observer para qualquer mudança no DOM
      this.observer = new MutationObserver((mutations) => {
        if (this.isUpdating) return;
        
        let needsUpdate = false;
        
        mutations.forEach(mutation => {
          // Verifica se novos elementos foram adicionados
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            needsUpdate = true;
          }
          
          // Verifica se classes foram removidas do html/body
          if (mutation.type === 'attributes' && 
              mutation.attributeName === 'class' &&
              (mutation.target === document.documentElement || mutation.target === document.body)) {
            needsUpdate = true;
          }
        });
        
        if (needsUpdate) {
          setTimeout(() => {
            this.ensureCursorActive();
          }, 200);
        }
      });
      
      this.observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class']
      });
      
      // Event listeners para navegação SPA
      window.addEventListener('popstate', this.handleNavigation);
      window.addEventListener('hashchange', this.handleNavigation);
      
      // Observer para mudanças na URL (para SPAs que não usam history API)
      let currentUrl = window.location.href;
      this.urlCheckInterval = setInterval(() => {
        if (window.location.href !== currentUrl) {
          currentUrl = window.location.href;
          setTimeout(() => this.ensureCursorActive(), 300);
        }
      }, 1000);
    },
    
    cleanup() {
      this.isUpdating = false;
      
      // Limpa os intervalos
      if (this.cursorInterval) {
        clearInterval(this.cursorInterval);
        this.cursorInterval = null;
      }
      
      if (this.urlCheckInterval) {
        clearInterval(this.urlCheckInterval);
        this.urlCheckInterval = null;
      }
      
      // Remove event listeners
      window.removeEventListener('popstate', this.handleNavigation);
      window.removeEventListener('hashchange', this.handleNavigation);
      
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
      
      // Marca como inativo no localStorage mas mantém as classes para persistir
      try {
        localStorage.setItem('customCursorActive', 'false');
      } catch (e) {
        if (window.customCursorSettings) {
          window.customCursorSettings.active = false;
        }
      }
    }
  }
}
</script>