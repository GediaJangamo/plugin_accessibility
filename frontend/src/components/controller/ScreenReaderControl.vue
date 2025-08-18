<template>
  <div 
    v-if="active"
    class="fixed bottom-5 left-1/2 transform -translate-x-1/2 z-50 transition-all duration-300 ease-in-out"
    aria-live="polite"
  >
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden w-auto max-w-4xl">
      <!-- Header com status e botão de fechar -->
      <div class="bg-gradient-to-r bg-[#3b82f6] p-3 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5L6 9H2v6h4l5 4V5zm10.293 2.707a1 1 0 00-1.414 1.414A5.978 5.978 0 0120 12a5.978 5.978 0 01-1.121 3.879 1 1 0 001.414 1.414A7.978 7.978 0 0022 12a7.978 7.978 0 00-1.707-4.293z" />
          </svg>
          <span class="text-white font-medium">{{ currentReadingStatus }}</span>
        </div>
        <button
          @click="closeReader" 
          class="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
          aria-label="Fechar leitor de tela"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-4">
        <!-- Controle de velocidade e modo de leitura -->
        <div class="flex items-center justify-between mb-4 gap-4">
          <!-- Modo de leitura -->
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-500 dark:text-gray-400">Modo</span>
            <div class="flex items-center rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
              <button 
                @click="setReadingMode('element')"
                :class="readingMode === 'element' ? 'bg-[#3b82f6] text-white' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'"
                class="px-3 py-1 text-xs font-medium transition-colors"
              >
                Elemento
              </button>
              <button 
                @click="setReadingMode('word')"
                :class="readingMode === 'word' ? 'bg-[#3b82f6] text-white' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'"
                class="px-3 py-1 text-xs font-medium transition-colors"
              >
                Palavra
              </button>
            </div>
          </div>

          <!-- Controle de velocidade -->
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-500 dark:text-gray-400">Velocidade</span>
            <div class="flex items-center rounded-full bg-gray-100 dark:bg-gray-700 overflow-hidden">
              <button 
                @click="decreaseRate"
                class="flex items-center justify-center p-2 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300"
                aria-label="Diminuir velocidade"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M20 12H4" />
                </svg>
              </button>
              <span class="w-14 text-center font-medium bg-[#3b82f6] text-white py-1.5">{{ speechRate.toFixed(1) }}x</span>
              <button 
                @click="increaseRate"
                class="flex items-center justify-center p-2 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300"
                aria-label="Aumentar velocidade"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Controles principais -->
        <div class="flex items-center gap-4 mb-3">
          <!-- Botão principal de play/pause -->
          <button 
            @click="playPause"
            class="flex-shrink-0 flex items-center justify-center bg-[#3b82f6] hover:bg-[#357ABD] text-white p-4 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#3b82f6]"
            :aria-label="isPlaying ? 'Pausar leitura' : 'Iniciar leitura'"
          >
            <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>

          <!-- Grupo de controles de navegação -->
          <div class="flex-1 flex items-center justify-between gap-2 bg-gray-50 dark:bg-gray-700 p-2 rounded-xl">
            <button 
              @click="previousElement"
              class="flex items-center justify-center bg-white dark:bg-gray-600 hover:bg-gray-100 dark:hover:bg-gray-500 text-[#3b82f6] dark:text-[#3b82f6] p-3 rounded-lg shadow-sm transition-colors"
              :aria-label="readingMode === 'word' ? 'Palavra anterior' : 'Elemento anterior'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            
            <!-- Botão de activar elemento ou entrar/sair -->
            <button 
              @click="activateElement"
              class="flex items-center justify-center text-white p-3 rounded-lg shadow-sm transition-colors"
              :class="getActivateButtonClass()"
              :aria-label="getActivateButtonLabel()"
            >
              <svg v-if="!isInContainer" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <!-- Ícone para entrar em container -->
              <svg v-else-if="canEnterCurrentContainer()" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              <!-- Ícone para sair de container -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
            
            <button 
              @click="restart"
              class="flex items-center justify-center bg-white dark:bg-gray-600 hover:bg-gray-100 dark:hover:bg-gray-500 text-red-500 p-3 rounded-lg shadow-sm transition-colors"
              aria-label="Reiniciar leitura"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            
            <button 
              @click="nextElement"
              class="flex items-center justify-center bg-white dark:bg-gray-600 hover:bg-gray-100 dark:hover:bg-gray-500 text-[#3b82f6] dark:text-[#3b82f6] p-3 rounded-lg shadow-sm transition-colors"
              :aria-label="readingMode === 'word' ? 'Próxima palavra' : 'Próximo elemento'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>

          <!-- Indicador de progresso -->
          <div class="flex-shrink-0 bg-gray-50 dark:bg-gray-700 px-4 py-3 rounded-lg text-center min-w-[80px]">
            <span class="text-gray-700 dark:text-gray-300 text-sm font-medium">
              {{ getProgressText() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScreenReaderControl",
  props: {
    active: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isPlaying: false,
      readableElements: [],
      currentElementIndex: -1,
      speechSynth: null,
      utterance: null,
      currentReadingStatus: "",
      speechRate: 1.0,
      gatherTimeout: null,
      observer: null,
      pauseTimer: null,
      isInitialized: false,
      keysEnabled: false,
      navigationDebounce: null,
      readingMode: 'element',
      currentWords: [],
      currentWordIndex: -1,
      wordHighlightSpan: null,
      // Navegação hierárquica
      isInContainer: false,
      containerStack: [],
      currentContainer: null,
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.$nextTick(() => {
            this.initReaderFeatures()
          })
        } else {
          this.cleanupReaderFeatures()
        }
      },
    },
  },

  mounted() {
  this.initMutationObserver();
  this.addCustomStyles();
  
  // Força o carregamento das vozes
  if (window.speechSynthesis) {
    this.loadVoices();
    window.speechSynthesis.onvoiceschanged = this.loadVoices;
  }

},

  beforeUnmount() {
    this.cleanupReaderFeatures()
    this.removeCustomStyles()
  },
  methods: {
    // Adiciona estilos customizados para os destaques
    addCustomStyles() {
      if (!document.getElementById('screen-reader-highlight-styles')) {
        const style = document.createElement('style')
        style.id = 'screen-reader-highlight-styles'
        style.textContent = `
          .sr-element-highlight {
            position: relative !important;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(147, 197, 253, 0.2)) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5), 0 0 25px rgba(59, 130, 246, 0.3) !important;
            transform: scale(1.02) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            z-index: 10 !important;
          }
          
          .sr-element-highlight::before {
            content: '' !important;
            position: absolute !important;
            top: -6px !important;
            left: -6px !important;
            right: -6px !important;
            bottom: -6px !important;
            background: linear-gradient(45deg, #3b82f6, #06b6d4) !important;
            border-radius: 14px !important;
            z-index: -1 !important;
            opacity: 0.4 !important;
            filter: blur(10px) !important;
            animation: sr-glow-pulse 2s ease-in-out infinite alternate !important;
          }
          
          .sr-word-highlight {
            background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
            color: white !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4) !important;
            transform: scale(1.05) !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
          }
          
          .sr-interactive-indicator::after {
            content: '⚡' !important;
            position: absolute !important;
            top: -8px !important;
            right: -8px !important;
            background: #10b981 !important;
            color: white !important;
            border-radius: 50% !important;
            width: 20px !important;
            height: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 10px !important;
            animation: sr-pulse 1s ease-in-out infinite !important;
          }

          .sr-container-indicator::after {
            content: '📁' !important;
            position: absolute !important;
            top: -8px !important;
            right: -8px !important;
            background: #8b5cf6 !important;
            color: white !important;
            border-radius: 50% !important;
            width: 20px !important;
            height: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 10px !important;
            animation: sr-pulse 1s ease-in-out infinite !important;
          }
            [data-screen-reader-ignore] {
            display: none !important;
            visibility: hidden !important;
          }
          /* Garante que todos elementos interativos tenham indicação visual */
            a, button, [role="button"], [tabindex="0"] {
              &:focus {
                outline: 2px solid #3b82f6;
                outline-offset: 2px;
              }
            }

            /* Estilo específico para Mac */
            @media (-webkit-mac-control) {
              [role="button"] {
                min-height: 24px; /* Melhora o target para click */
              }
            }
          
          @keyframes sr-glow-pulse {
            0% { opacity: 0.3; transform: scale(1); }
            100% { opacity: 0.6; transform: scale(1.01); }
          }
          
          @keyframes sr-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
          }
        `
        document.head.appendChild(style)
      }
    },
    
    // Remove estilos customizados
    removeCustomStyles() {
      const style = document.getElementById('screen-reader-highlight-styles')
      if (style) {
        style.remove()
      }
    },

    // Verifica se é um container (accordion, tabs, etc.)
    isContainer(element) {
      const containerSelectors = [
        '.accordion-item',
        '.accordion',
        '.tab-pane',
        '.tabs',
        '.collapse',
        '.modal-body',
        '.dropdown-menu',
        '.card-body',
        '.sidebar',
        '.nav-tabs',
        '.nav-pills'
      ]
      
      return containerSelectors.some(selector => 
        element.matches && element.matches(selector)
      )
    },

    // Verifica se pode entrar no container atual
    canEnterCurrentContainer() {
    if (this.currentElementIndex < 0 || !this.readableElements[this.currentElementIndex]) {
      return false
    }
    
    const element = this.readableElements[this.currentElementIndex]
    
    // Verifica se é um accordion expandido
    if (this.isAccordionButton(element)) {
      return true // Permite entrar mesmo se não estiver expandido
    }
    
    return this.isContainer(element) || this.hasExpandableContent(element)
    },
    // Verifica se tem conteúdo expansível
    hasExpandableContent(element) {
      // Accordion buttons
      if (element.classList.contains('accordion-button')) {
        return true
      }
      
      // Elementos com data-bs-toggle
      if (element.getAttribute('data-bs-toggle')) {
        return true
      }
      
      // Elementos que controlam outros elementos
      const controls = element.getAttribute('aria-controls')
      if (controls) {
        const controlled = document.getElementById(controls)
        return controlled && controlled.children.length > 0
      }
      
      return false
    },

    // Função melhorada para entrar no container
    enterContainer() {
      if (this.currentElementIndex < 0 || !this.readableElements[this.currentElementIndex]) {
        return;
      }

      const element = this.readableElements[this.currentElementIndex];
      const elementName = this.getElementText(element).replace('botão', '').replace('link', '').trim();
      
      // Verifica se é um accordion não expandido
      if (this.isAccordionButton(element)) {
        if (element.getAttribute('aria-expanded') === 'false') {
          this.announceChange(`Expandindo ${elementName}...`);
          
          // Força o clique no elemento - método mais direto
          this.triggerClick(element);
          
          // Aguarda a animação sem entrar automaticamente
          setTimeout(() => {
            if (element.getAttribute('aria-expanded') === 'true') {
              this.announceChange(`${elementName} expandido. Navegue para o botão Entrar se desejar acessar o conteúdo.`);
              this.gatherReadableElements(); // Atualiza a lista de elementos
            } else {
              this.announceChange(`Falha ao expandir ${elementName}`);
            }
          }, 350);
          return; // Importante: não prossegue para enterContainer automaticamente
        }
      }

      // Lógica para containers normais ou accordions já expandidos
      this.proceedToEnterContainer(element);
    },

    // Método melhorado para trigger de clique
    triggerClick(element) {
      // Para MacBook Air, precisamos simular o clique de forma mais explícita
      try {
        // Método 1: Clique direto
        element.click();
        
        // Se não funcionou, tenta métodos alternativos
        setTimeout(() => {
          if (this.isAccordionButton(element) && element.getAttribute('aria-expanded') === 'false') {
            // Método 2: Disparo de evento personalizado
            const clickEvent = new MouseEvent('click', {
              view: window,
              bubbles: true,
              cancelable: true
            });
            element.dispatchEvent(clickEvent);
            
            // Método 3: Para Bootstrap especificamente
            if (element.getAttribute('data-bs-toggle') === 'collapse') {
              const targetId = element.getAttribute('data-bs-target') || element.getAttribute('aria-controls');
              if (targetId) {
                const target = document.querySelector(targetId) || document.getElementById(targetId.replace('#', ''));
                if (target && window.bootstrap) {
                  // Usa a API do Bootstrap diretamente se disponível
                  const bsCollapse = window.bootstrap.Collapse.getOrCreateInstance(target);
                  bsCollapse.toggle();
                }
              }
            }
          }
        }, 100);
      } catch (error) {
        console.error('Erro ao disparar clique:', error);
        this.announceChange('Erro ao ativar elemento');
      }
    },

    // Procede para entrar no container
    proceedToEnterContainer(element) {
  // Salva o estado atual
  this.containerStack.push({
    container: this.currentContainer,
    elements: [...this.readableElements],
    index: this.currentElementIndex
  })

  this.currentContainer = element
  this.isInContainer = true

  // Encontra os elementos dentro do container
  let containerContent = null
  
  if (this.isAccordionButton(element)) {
    const controls = element.getAttribute('aria-controls')
    if (controls) {
      containerContent = document.getElementById(controls)
    }
  } else if (this.isContainer(element)) {
    containerContent = element
  }

  if (containerContent) {
    this.gatherElementsInContainer(containerContent)
    this.currentElementIndex = 0
    this.announceChange(`Entrando no container com ${this.readableElements.length} elementos`)
    
    if (this.readableElements.length > 0) {
      this.highlightCurrentElement()
    }
  } else {
    this.announceChange("Container vazio")
  }
},

    // Sai do container atual
    exitContainer() {
      const containerName = this.getElementText(this.currentContainer);
      this.announceChange(`Saindo de ${containerName}`);

      if (this.containerStack.length === 0) {
        this.announceChange("Já está no nível principal")
        return
      }

      const previousState = this.containerStack.pop()
      
      this.currentContainer = previousState.container
      this.readableElements = previousState.elements
      this.currentElementIndex = previousState.index
      this.isInContainer = this.containerStack.length > 0

      this.announceChange("Saindo do container")
      this.highlightCurrentElement()
      this.updateReadingStatus()
    },

    // Função melhorada para detectar botões de accordion
    isAccordionButton(element) {
    return (
      element.classList.contains('accordion-button') || 
      (element.getAttribute('data-bs-toggle') === 'collapse' && element.getAttribute('aria-controls')) ||
      (element.getAttribute('data-toggle') === 'collapse' && element.getAttribute('aria-controls')) ||
      (element.getAttribute('aria-expanded') !== null && element.getAttribute('aria-controls'))
    )
},

    // Coleta elementos dentro de um container específico
    gatherElementsInContainer(container) {

      const selector = `
        img,
        svg[aria-label],
        h1, h2, h3, h4, h5, h6,
        p:not(.accordion-body p, .collapse:not(.show) p, .tab-pane:not(.active) p),
        a:not([aria-hidden="true"]):not(.accordion-body a, .collapse:not(.show) a, .tab-pane:not(.active) a),
        button,
        input[type="text"], input[type="email"], input[type="password"], input[type="search"],
        textarea,
        select,
        label:not(.accordion-body label, .collapse:not(.show) label, .tab-pane:not(.active) label),
        li:not(.accordion-body li, .collapse:not(.show) li, .tab-pane:not(.active) li),
        td:not(.accordion-body td, .collapse:not(.show) td, .tab-pane:not(.active) td),
        th:not(.accordion-body th, .collapse:not(.show) th, .tab-pane:not(.active) th),
        span.badge:not(.accordion-body span.badge, .collapse:not(.show) span.badge, .tab-pane:not(.active) span.badge),
        .accordion-button,
        .nav-link,
        .tab-button,
        .card-title:not(.accordion-body .card-title, .collapse:not(.show) .card-title, .tab-pane:not(.active) .card-title),
        .card-text:not(.accordion-body .card-text, .collapse:not(.show) .card-text, .tab-pane:not(.active) .card-text)
      `
      
      const elements = Array.from(container.querySelectorAll(selector))
      
      this.readableElements = elements.filter(el => {
        // Ignora elementos do próprio leitor
        if (el.closest('.screen-reader-control') || el.closest('[data-screen-reader-ignore]')) {
          return false
        }
        
        const text = this.getElementText(el)
        if (!text || text.trim().length === 0) {
          return false
        }
        
        // Verifica visibilidade
        const style = window.getComputedStyle(el)
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
          return false
        }
        
        return true
      }).sort((a, b) => {
        const rectA = a.getBoundingClientRect()
        const rectB = b.getBoundingClientRect()
        
        if (Math.abs(rectA.top - rectB.top) > 10) {
          return rectA.top - rectB.top
        }
        return rectA.left - rectB.left
      })

      this.readableElements = this.removeDuplicateElements(this.readableElements)
    },

    // Retorna classe do botão de ativar baseado no contexto
    getActivateButtonClass() {
      if (this.isInContainer) {
        return 'bg-orange-500 hover:bg-orange-600'  // Sair do container
      } else if (this.canEnterCurrentContainer()) {
        return 'bg-purple-500 hover:bg-purple-600'  // Entrar no container
      } else if (this.canActivateCurrentElement()) {
        return 'bg-green-500 hover:bg-green-600'    // Ativar elemento
      } else {
        return 'bg-gray-400 cursor-not-allowed'     // Desabilitado
      }
    },

    // Retorna label do botão de ativar baseado no contexto
    getActivateButtonLabel() {
      if (this.isInContainer) {
        return 'Sair do container (Esc)'
      } else if (this.canEnterCurrentContainer()) {
        return 'Entrar no container (Enter)'
      } else if (this.canActivateCurrentElement()) {
        return 'Ativar elemento (Enter)'
      } else {
        return 'Elemento não interativo'
      }
    },

    // Verifica se o elemento atual pode ser ativado
    canActivateCurrentElement() {
      if (this.currentElementIndex < 0 || !this.readableElements[this.currentElementIndex]) {
        return false
      }
      
      return this.isInteractiveElement(this.readableElements[this.currentElementIndex])
    },

    // Verifica se um elemento é interativo
    isInteractiveElement(element) {
      const tag = element.tagName.toLowerCase()
      const interactiveTags = ['button', 'a', 'input', 'textarea', 'select']
      
      // Verifica se é um botão de accordion do Bootstrap
      if (element.classList.contains('accordion-button') || 
          element.getAttribute('data-bs-toggle') === 'collapse') {
        return true
      }
      
      if (interactiveTags.includes(tag)) {
        return true
      }
      
      const role = element.getAttribute('role')
      if (role && ['button', 'link', 'tab', 'menuitem'].includes(role)) {
        return true
      }
      
      if (element.onclick || element.getAttribute('data-bs-toggle')) {
        return true
      }
      
      return false
    },

    // Função principal melhorada para ativação de elementos
   
  activateElement() {
  if (this.isInContainer) {
    this.exitContainer()
    return
  }

  if (this.currentElementIndex < 0 || !this.readableElements[this.currentElementIndex]) {
    return
  }

  const element = this.readableElements[this.currentElementIndex]
  
  // Tratamento específico para accordions
  if (this.isAccordionButton(element)) {
    // Foca no elemento primeiro para garantir que eventos de teclado funcionem
    element.focus()
    this.handleAccordionButton(element)
    return
  }

  // Tratamento para links e botões normais
  if (this.isRegularInteractiveElement(element)) {
    element.focus()
    this.activateInteractiveElement(element)
    return
  }

  // Entrada em containers genéricos
  if (this.canEnterCurrentContainer()) {
    element.focus()
    this.enterContainer()
  }
},

   // Função melhorada para lidar com botões de accordion
  handleAccordionButton(button) {
    const accordionTitle = this.getElementText(button).replace('botão', '').replace('Botão:', '').trim()
    const wasExpanded = button.getAttribute('aria-expanded') === 'true'
    
    this.announceChange(`${wasExpanded ? 'Recolhendo' : 'Expandindo'} ${accordionTitle}...`)
    
    // Primeiro tenta usar a API do Bootstrap se disponível
    if (window.bootstrap && window.bootstrap.Collapse) {
      try {
        const targetId = button.getAttribute('data-bs-target') || 
                      button.getAttribute('aria-controls') || 
                      button.getAttribute('data-target')
        const selector = targetId?.startsWith('#') ? targetId : `#${targetId}`
        const target = selector ? document.querySelector(selector) : null
        
        if (target) {
          const bsCollapse = window.bootstrap.Collapse.getOrCreateInstance(target, {
            toggle: false
          })
          
          // Força a abertura/fechamento imediato
          if (wasExpanded) {
            bsCollapse.hide()
          } else {
            bsCollapse.show()
          }
          
          // Atualiza o estado após a animação
          setTimeout(() => {
            const isNowExpanded = button.getAttribute('aria-expanded') === 'true'
            const newStatus = isNowExpanded ? 'expandido' : 'recolhido'
            this.announceChange(`${accordionTitle} ${newStatus}`)
            
            // Se for um accordion pai, atualiza a lista de elementos
            if (!target.closest('.accordion-collapse')) {
              this.gatherReadableElements()
            }
          }, 350)
          return
        }
      } catch (e) {
        console.error('Erro ao usar API Bootstrap:', e)
      }
    }
    
    // Método alternativo robusto
    this.forceAccordionToggle(button)
    
    // Feedback imediato
    setTimeout(() => {
      const isNowExpanded = button.getAttribute('aria-expanded') === 'true'
      const newStatus = isNowExpanded ? 'expandido' : 'recolhido'
      this.announceChange(`${accordionTitle} ${newStatus}`)
      
      // Se for um accordion pai, atualiza a lista de elementos
      if (!button.closest('.accordion-collapse')) {
        this.gatherReadableElements()
      }
    }, 350)
  },
    // Método robusto para forçar o toggle do accordion
  forceAccordionToggle(button) {
  try {
    // Dispara um clique completo (mousedown + mouseup + click)
    ['mousedown', 'mouseup', 'click'].forEach(eventType => {
      const event = new MouseEvent(eventType, {
        bubbles: true,
        cancelable: true,
        view: window
      })
      button.dispatchEvent(event)
    })
    
    // Alterna manualmente os atributos imediatamente
    const targetId = button.getAttribute('data-bs-target') || 
                    button.getAttribute('aria-controls') || 
                    button.getAttribute('data-target')
    const selector = targetId?.startsWith('#') ? targetId : `#${targetId}`
    const target = selector ? document.querySelector(selector) : null
    
    if (target) {
      const wasExpanded = button.getAttribute('aria-expanded') === 'true'
      button.setAttribute('aria-expanded', !wasExpanded)
      
      // Adiciona/remove classes diretamente para feedback visual imediato
      if (wasExpanded) {
        target.classList.remove('show')
        button.classList.add('collapsed')
      } else {
        target.classList.add('show')
        button.classList.remove('collapsed')
      }
    }
  } catch (error) {
    console.error('Erro ao alternar accordion:', error)
    this.announceChange('Erro ao ativar accordion')
  }
},

    isRegularInteractiveElement(element) {
      const tag = element.tagName.toLowerCase()
      return (
        (tag === 'a' && element.href) || 
        (tag === 'button' && !this.isAccordionButton(element)) ||
        ['input', 'textarea', 'select'].includes(tag)
      )
    },

    activateInteractiveElement(element) {
      const elementName = this.getElementText(element)
      this.announceChange(`Ativando ${elementName}`)
      
      this.triggerClick(element)
      
      setTimeout(() => this.gatherReadableElements(), 300)
    },

    // Define o modo de leitura
    setReadingMode(mode) {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.readingMode = mode
      
      if (mode === 'word' && this.currentElementIndex >= 0) {
        this.setupWordReading()
      } else {
        this.currentWords = []
        this.currentWordIndex = -1
      }
      
      this.updateReadingStatus()
    },

    // Configura a leitura palavra por palavra
    setupWordReading() {
      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        const text = this.getElementText(element)
        this.currentWords = text.split(/\s+/).filter(word => word.length > 0)
        this.currentWordIndex = 0
        this.highlightCurrentWord()
      }
    },

    // Retorna o texto de progresso baseado no modo
    getProgressText() {
      if (this.readingMode === 'word' && this.currentWords.length > 0) {
        return `${this.currentWordIndex + 1}/${this.currentWords.length}`
      } else if (this.readableElements.length > 0) {
        return this.currentElementIndex >= 0 ? `${this.currentElementIndex + 1}/${this.readableElements.length}` : '0/0'
      }
      return '0/0'
    },

    // Método para fechar o leitor de tela
    closeReader() {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.$emit('update:screenReader', false)
    },
    
    // Inicializa todos os recursos do leitor
    initReaderFeatures() {
      this.initializeSpeechSynthesis()

      setTimeout(() => {
        this.resetToMainLevel()
        this.gatherReadableElements()
        this.currentElementIndex = -1
        this.removeAllHighlights()
        this.enableKeyboardControls()
        this.isInitialized = true
      }, 300)
    },

    // Reseta para o nível principal
    resetToMainLevel() {
      this.isInContainer = false
      this.containerStack = []
      this.currentContainer = null
    },

    // Limpa todos os recursos do leitor
    cleanupReaderFeatures() {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.disableKeyboardControls()
      this.resetToMainLevel()

      if (this.observer) {
        this.observer.disconnect()
      }

      this.isInitialized = false
    },

    // Inicializa o observador de mudanças no DOM
    initMutationObserver() {
      if (window.MutationObserver) {
        this.observer = new MutationObserver(this.debounceGatherElements)
        this.observer.observe(document.body, {
          childList: true,
          subtree: true,
          attributes: true,
          attributeFilter: ['class', 'style', 'aria-expanded']
        })
      }
      // Verifica se o Bootstrap está carregado
      if (!window.bootstrap) {
        console.warn('Bootstrap não detectado - usando métodos alternativos para accordions')
      }
    },

    // Ativa os comandos de teclado
    enableKeyboardControls() {
      if (!this.keysEnabled) {
        document.addEventListener("keydown", this.handleKeyboardShortcuts)
        this.keysEnabled = true
      }
    },

    // Desativa os comandos de teclado
    disableKeyboardControls() {
      document.removeEventListener("keydown", this.handleKeyboardShortcuts)
      this.keysEnabled = false
    },

    // Inicializa a API de síntese de fala
    initializeSpeechSynthesis() {
      if ("speechSynthesis" in window) {
        this.speechSynth = window.speechSynthesis

        if (this.speechSynth.onvoiceschanged !== undefined) {
          this.speechSynth.onvoiceschanged = this.loadVoices
        }

        this.loadVoices()
      } else {
        console.error("API de Síntese de Fala não suportada no navegador")
        this.currentReadingStatus = "Leitor não suportado"
      }
    },

//    loadVoices() {
//   if (this.speechSynth) {
//     // Força a atualização das vozes (necessário em alguns navegadores)
//     const voices = this.speechSynth.getVoices();
    
//     // Tenta encontrar uma voz feminina em português
//     this.femaleVoice = voices.find(voice => {
//       const isPortuguese = voice.lang.includes("pt-BR") || voice.lang.includes("pt");
//       const isFemale = voice.name.toLowerCase().includes("female") || 
//                       voice.name.includes("Maria") || 
//                       voice.name.includes("Luciana") || 
//                       voice.name.includes("Vitória");
//       return isPortuguese && isFemale;
//     });

//     // Se não encontrar, usa qualquer voz em português
//     if (!this.femaleVoice) {
//       this.femaleVoice = voices.find(voice => voice.lang.includes("pt"));
//     }
//   }
// },
// loadVoices() {
//   if (!this.speechSynth) return;

//   // Força a atualização das vozes (necessário em alguns navegadores)
//   const voices = this.speechSynth.getVoices();
  
//   // Tenta encontrar uma voz feminina em português
//   this.femaleVoice = voices.find(voice => {
//     const isPortuguese = voice.lang.includes("pt-BR") || voice.lang.includes("pt");
//     const isFemale = voice.name.toLowerCase().includes("female") || 
//                     voice.name.includes("Maria") || 
//                     voice.name.includes("Luciana") || 
//                     voice.name.includes("Vitória");
//     return isPortuguese && isFemale;
//   });

//   // Se não encontrar, usa qualquer voz em português
//   if (!this.femaleVoice) {
//     this.femaleVoice = voices.find(voice => voice.lang.includes("pt"));
//   }

//   // Se ainda não encontrou, usa a primeira voz disponível
//   if (!this.femaleVoice && voices.length > 0) {
//     this.femaleVoice = voices[0];
//   }
// },
loadVoices() {
  if (!this.speechSynth) return;

  // Força a atualização em navegadores que precisam
  const voices = this.speechSynth.getVoices();
  
  // Tenta encontrar a voz feminina em português
  this.femaleVoice = voices.find(voice => {
    // Verifica por idioma
    const isPortuguese = voice.lang.includes("pt-BR") || 
                        voice.lang.includes("pt-PT") || 
                        voice.lang.includes("pt");
    
    // Verifica por nomes comuns de vozes femininas
    const isFemale = voice.name.toLowerCase().includes("female") || 
                    /(Maria|Luciana|Vitória|Heloísa|Fernanda|Isabela)/i.test(voice.name);
    
    return isPortuguese && isFemale;
  });

  // Se não encontrou, pega qualquer voz em português
  if (!this.femaleVoice) {
    this.femaleVoice = voices.find(voice => 
      voice.lang.includes("pt-BR") || 
      voice.lang.includes("pt-PT") || 
      voice.lang.includes("pt")
    );
  }

  // Se ainda não encontrou, pega a primeira voz disponível
  if (!this.femaleVoice && voices.length > 0) {
    this.femaleVoice = voices[0];
  }
},
    // Obtém o texto adequado para leitura de um elemento
    getElementText(element) {
      const tag = element.tagName.toLowerCase()
      
      if (tag === 'img') {
        const alt = element.alt?.trim()
        const title = element.title?.trim()
        const src = element.src
        
        if (alt) {
          return `Imagem: ${alt}`
        } else if (title) {
          return `Imagem: ${title}`
        } else if (src) {
          const filename = src.split('/').pop().split('?')[0]
          return `Imagem: ${filename}`
        } else {
          return 'Imagem sem descrição'
        }
      }
      
      if (tag === 'svg') {
        return element.getAttribute('aria-label') || 'Gráfico sem descrição'
      }
      
      if (this.isInteractiveElement(element)) {
        const text = element.textContent.trim()
        if (tag === 'button') {
          return `Botão: ${text}`
        } else if (tag === 'a') {
          return `Link: ${text}`
        } else {
          return `Elemento clicável: ${text}`
        }
      }

      // Se é um container, indica isso no texto
      if (this.isContainer(element) || this.hasExpandableContent(element)) {
        const text = element.textContent.trim()
        return `Área expandível: ${text}`
      }
      
      return element.textContent.trim()
    },

    // Coleta elementos que podem ser lidos
    gatherReadableElements() {
      // Primeiro, remova todos os atributos de ignorar temporariamente
      document.querySelectorAll('[data-screen-reader-ignore]').forEach(el => {
        el.removeAttribute('data-screen-reader-ignore')
      })

      // Depois adicione apenas nos accordions colapsados
      document.querySelectorAll('.collapse:not(.show), .tab-pane:not(.active)').forEach(el => {
        el.setAttribute('data-screen-reader-ignore', 'true')
      })

      // Seletor atualizado para elementos legíveis
      const selector = `
        img,
        svg[aria-label],
        h1, h2, h3, h4, h5, h6,
        p:not([data-screen-reader-ignore] p),
        a:not([aria-hidden="true"]):not([data-screen-reader-ignore] a),
        button,
        input[type="text"], input[type="email"], input[type="password"], input[type="search"],
        textarea,
        select,
        label:not([data-screen-reader-ignore] label),
        li:not([data-screen-reader-ignore] li),
        td:not([data-screen-reader-ignore] td),
        th:not([data-screen-reader-ignore] th),
        span.badge:not([data-screen-reader-ignore] span.badge),
        .accordion-button,
        .nav-link,
        .tab-button,
        .card-title:not([data-screen-reader-ignore] .card-title),
        .card-text:not([data-screen-reader-ignore] .card-text)
      `
      
      // Restante da lógica de coleta de elementos...
      const mainContent = document.getElementById("main-content") || document.body
      const allElements = Array.from(mainContent.querySelectorAll(selector))
      
      this.readableElements = allElements.filter(el => {
        // Ignora elementos marcados para ignorar
        if (el.closest('[data-screen-reader-ignore]')) {
          return false
        }
        
        // Verifica se o elemento tem conteúdo legível
        const text = this.getElementText(el)
        if (!text || text.trim().length === 0) {
          return false
        }
        
        // Verifica visibilidade
        const style = window.getComputedStyle(el)
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
          return false
        }
        
        return true
      }).sort((a, b) => {
        // Ordenação por posição na página
        const rectA = a.getBoundingClientRect()
        const rectB = b.getBoundingClientRect()
        
        if (Math.abs(rectA.top - rectB.top) > 10) {
          return rectA.top - rectB.top
        }
        return rectA.left - rectB.left
      })

      this.readableElements = this.removeDuplicateElements(this.readableElements)
    },

    // Remove elementos duplicados
    removeDuplicateElements(elements) {
      const seen = new Map()
      
      return elements.filter(el => {
        const text = this.getElementText(el).toLowerCase().trim()
        const tag = el.tagName.toLowerCase()
        
        // Para imagens, usa src como chave adicional
        if (tag === 'img') {
          const key = `${tag}:${text}:${el.src}`
          if (seen.has(key)) return false
          seen.set(key, true)
          return true
        }
        
        // Para outros elementos, verifica por texto e posição
        const key = `${tag}:${text}`
        
        if (seen.has(key)) {
          return false
        }
        
        seen.set(key, true)
        return true
      })
    },

    debounceGatherElements() {
      if (this.gatherTimeout) clearTimeout(this.gatherTimeout)
      this.gatherTimeout = setTimeout(() => {
        if (this.active && !this.isInContainer) {
          // Só recoleta elementos se não estiver dentro de um container
          this.gatherReadableElements()
        }
      }, 500)
    },

//     playPause() {
//   if (!this.speechSynth) return;
  
//   if (this.speechSynth.paused) {
//     this.resumeSpeaking();
//   } else if (this.isPlaying) {
//     this.pauseSpeaking();
//   } else {
//     if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
//       this.currentElementIndex = 0;
//       if (this.readingMode === 'word') {
//         this.setupWordReading();
//       } else {
//         this.highlightCurrentElement();
//       }
//     }
//     this.speakCurrent();
//   }
// },
playPause() {
  if (!this.speechSynth) return;

  // Caso 1: Está pausado -> Retomar
  if (this.speechSynth.paused) {
    this.resumeSpeaking();
    return;
  }

  // Caso 2: Está falando -> Pausar
  if (this.speechSynth.speaking) {
    this.pauseSpeaking();
    return;
  }

  // Caso 3: Não está falando -> Começar do elemento atual
  this.startSpeakingFromCurrent();
},

startSpeakingFromCurrent() {
  if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
    this.currentElementIndex = 0;
  }

  if (this.readableElements.length > 0) {
    if (this.readingMode === 'word') {
      this.setupWordReading();
    }
    this.highlightCurrentElement();
    this.speakCurrent();
  }
},
    // Navega para o elemento/palavra anterior
    // previousElement() {
    //   if (this.navigationDebounce) return
    //   this.navigationDebounce = setTimeout(() => {
    //     this.navigationDebounce = null
    //   }, 200)

    //   this.stopSpeaking()

    //   if (this.readingMode === 'word') {
    //     if (this.currentWordIndex > 0) {
    //       this.currentWordIndex--
    //       this.highlightCurrentWord()
    //     } else if (this.currentElementIndex > 0) {
    //       this.currentElementIndex--
    //       this.setupWordReading()
    //     }
    //   } else {
    //     if (this.currentElementIndex > 0) {
    //       this.currentElementIndex--
    //       this.highlightCurrentElement()
    //     }
    //   }

    //   this.updateReadingStatus()

    //   if (this.isPlaying) {
    //     setTimeout(() => {
    //       if (this.isPlaying) {
    //         this.speakCurrent()
    //       }
    //     }, 100)
    //   }
    // },
//     previousElement() {
//   if (this.navigationDebounce) return;
//   this.navigationDebounce = setTimeout(() => {
//     this.navigationDebounce = null;
//   }, 200);

//   this.stopSpeaking();

//   if (this.readingMode === 'word') {
//     if (this.currentWordIndex > 0) {
//       this.currentWordIndex--;
//     } else if (this.currentElementIndex > 0) {
//       this.currentElementIndex--;
//       this.setupWordReading();
//     }
//   } else {
//     if (this.currentElementIndex > 0) {
//       this.currentElementIndex--;
//     }
//   }

//   // Garante que o índice não fique negativo
//   if (this.currentElementIndex < 0) {
//     this.currentElementIndex = 0;
//   }

//   this.updateReadingStatus();
//   this.highlightCurrentElement();

//   if (this.isPlaying) {
//     // Pequeno delay para garantir que o highlight foi aplicado
//     setTimeout(() => {
//       if (this.isPlaying) {
//         this.speakCurrent();
//       }
//     }, 100);
//   }
// },

previousElement() {
  this.stopSpeaking();

  if (this.readingMode === 'word') {
    if (this.currentWordIndex > 0) {
      this.currentWordIndex--;
    } else if (this.currentElementIndex > 0) {
      this.currentElementIndex--;
      this.setupWordReading();
    }
  } else {
    if (this.currentElementIndex > 0) {
      this.currentElementIndex--;
    }
  }

  // Garante que não fique com índice negativo
  this.currentElementIndex = Math.max(0, this.currentElementIndex);
  
  this.updateReadingStatus();
  this.highlightCurrentElement();

  // Se estava tocando, continua a leitura
  if (this.isPlaying) {
    setTimeout(() => this.speakCurrent(), 100);
  }
},
    // Navega para o próximo elemento/palavra
    nextElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.readingMode === 'word') {
        if (this.currentWordIndex < this.currentWords.length - 1) {
          this.currentWordIndex++
          this.highlightCurrentWord()
        } else if (this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++
          this.setupWordReading()
        }
      } else {
        if (this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++
          this.highlightCurrentElement()
        }
      }

      this.updateReadingStatus()

      if (this.isPlaying) {
        setTimeout(() => {
          if (this.isPlaying) {
            this.speakCurrent()
          }
        }, 100)
      }
    },

    // Reinicia a leitura do primeiro elemento
    restart() {
      this.stopSpeaking()

      if (this.readableElements.length > 0) {
        this.currentElementIndex = 0
        if (this.readingMode === 'word') {
          this.setupWordReading()
        } else {
          this.highlightCurrentElement()
        }
        this.updateReadingStatus()

        if (this.isPlaying) {
          this.speakCurrent()
        }
      }
    },

    // Fala o elemento ou palavra atual
    // async speakCurrent() {
    //   if (this.readingMode === 'word') {
    //     await this.speakCurrentWord()
    //   } else {
    //     await this.speakCurrentElement()
    //   }
    // },
    async speakCurrent() {
  if (!this.speechSynth) return;

  // Garante que as vozes estão carregadas
  await this.ensureVoicesLoaded();

  // Configura a voz antes de cada fala
  this.setupVoice();

  if (this.readingMode === 'word') {
    await this.speakCurrentWord();
  } else {
    await this.speakCurrentElement();
  }
},

setupVoice() {
  if (!this.utterance) return;

  // Prioridade para voz feminina em português
  if (this.femaleVoice) {
    this.utterance.voice = this.femaleVoice;
    this.utterance.lang = "pt-BR";
  } else {
    // Fallback para qualquer voz em português
    const voices = this.speechSynth.getVoices();
    const portugueseVoice = voices.find(v => v.lang.includes('pt'));
    if (portugueseVoice) {
      this.utterance.voice = portugueseVoice;
      this.utterance.lang = portugueseVoice.lang;
    }
  }
},

    // Lê em voz alta a palavra atual

    speakCurrentWord() {
  if (!this.speechSynth || this.currentWordIndex < 0 || this.currentWordIndex >= this.currentWords.length) {
    return;
  }

  this.stopSpeaking();

  const word = this.currentWords[this.currentWordIndex];
  this.utterance = new SpeechSynthesisUtterance(word);

  // Sempre usar a voz feminina
  if (this.femaleVoice) {
    this.utterance.voice = this.femaleVoice;
  }

  this.utterance.rate = this.speechRate;
  this.utterance.pitch = 1.0;
  this.utterance.lang = "pt-BR";

  // Manter referência ao componente Vue
  const self = this;

  this.utterance.onend = function() {
    if (self.active && self.isPlaying) {
      if (self.currentWordIndex < self.currentWords.length - 1) {
        self.currentWordIndex++;
        self.highlightCurrentWord();
        self.updateReadingStatus();
        self.speakCurrentWord();
      } else if (self.currentElementIndex < self.readableElements.length - 1) {
        self.currentElementIndex++;
        self.setupWordReading();
        self.updateReadingStatus();
        self.speakCurrentWord();
      } else {
        self.isPlaying = false;
        self.currentReadingStatus = "Leitura concluída";
      }
    }
  };

  this.utterance.onerror = function(event) {
    console.error("Erro na síntese de fala:", event);
    self.isPlaying = false;
    self.currentReadingStatus = "Erro na leitura";
  };

  this.highlightCurrentWord();
  this.speechSynth.speak(this.utterance);
  this.isPlaying = true;
  this.updateReadingStatus();
},
async speakCurrentElement() {
  if (!this.speechSynth || this.currentElementIndex < 0) return;

  this.stopSpeaking();
  await this.ensureVoicesLoaded();

  const element = this.readableElements[this.currentElementIndex];
  const textToSpeak = this.getElementText(element);

  this.utterance = new SpeechSynthesisUtterance(textToSpeak);
  this.setupVoice();

  this.utterance.rate = this.speechRate;
  this.utterance.pitch = 1.0;

  const self = this;
  this.utterance.onboundary = function(event) {
    if (event.name === 'word') {
      self.highlightCurrentWord();
    }
  };

  this.utterance.onend = function() {
    if (self.active && self.isPlaying) {
      if (self.currentElementIndex < self.readableElements.length - 1) {
        self.currentElementIndex++;
        self.highlightCurrentElement();
        self.updateReadingStatus();
        self.speakCurrentElement();
      } else {
        self.isPlaying = false;
        self.currentReadingStatus = "Leitura concluída";
      }
    }
  };

  this.utterance.onerror = function(event) {
    console.error("Erro na síntese de fala:", event);
    self.isPlaying = false;
    self.currentReadingStatus = "Erro na leitura";
  };

  this.highlightCurrentElement();
  this.speechSynth.speak(this.utterance);
  this.isPlaying = true;
  this.updateReadingStatus();
},
// async speakCurrentElement() {
//   if (!this.speechSynth || this.currentElementIndex < 0 || 
//       this.currentElementIndex >= this.readableElements.length) {
//     return;
//   }

//   this.stopSpeaking();

//   // Garante que as vozes estão carregadas
//   await this.ensureVoicesLoaded();

//   const element = this.readableElements[this.currentElementIndex];
//   const textToSpeak = this.getElementText(element);

//   this.utterance = new SpeechSynthesisUtterance(textToSpeak);

//   // Sempre usar a voz feminina
//   if (this.femaleVoice) {
//     this.utterance.voice = this.femaleVoice;
//   } else {
//     // Fallback: tentar encontrar qualquer voz em português
//     const voices = this.speechSynth.getVoices();
//     const portugueseVoice = voices.find(v => v.lang.includes('pt'));
//     if (portugueseVoice) this.utterance.voice = portugueseVoice;
//   }

//   // Configurações da fala
//   this.utterance.rate = this.speechRate;
//   this.utterance.pitch = 1.0;
//   this.utterance.lang = "pt-BR";

//   // Configura os callbacks
//   const self = this;
//   this.utterance.onend = function() {
//     if (self.active && self.isPlaying) {
//       if (self.currentElementIndex < self.readableElements.length - 1) {
//         self.currentElementIndex++;
//         self.highlightCurrentElement();
//         self.updateReadingStatus();
//         self.speakCurrentElement();
//       } else {
//         self.isPlaying = false;
//         self.currentReadingStatus = "Leitura concluída";
//       }
//     }
//   };

//   this.utterance.onerror = function(event) {
//     console.error("Erro na síntese de fala:", event);
//     self.isPlaying = false;
//     self.currentReadingStatus = "Erro na leitura";
//   };

//   this.highlightCurrentElement();
//   this.speechSynth.speak(this.utterance);
//   this.isPlaying = true;
//   this.updateReadingStatus();
// },

// Novo método para garantir que as vozes estão carregadas
// ensureVoicesLoaded() {
//   return new Promise((resolve) => {
//     const voices = this.speechSynth.getVoices();
//     if (voices.length > 0) {
//       resolve();
//     } else {
//       this.speechSynth.onvoiceschanged = () => {
//         this.loadVoices();
//         resolve();
//       };
//     }
//   });
// },

ensureVoicesLoaded() {
  return new Promise((resolve) => {
    const voices = this.speechSynth.getVoices();
    if (voices.length > 0) {
      this.loadVoices();
      resolve();
    } else {
      this.speechSynth.onvoiceschanged = () => {
        this.loadVoices();
        resolve();
      };
    }
  });
},

//     speakCurrentElement() {
//   if (!this.speechSynth || this.currentElementIndex < 0 || 
//       this.currentElementIndex >= this.readableElements.length) {
//     return;
//   }

//   this.stopSpeaking();

//   const element = this.readableElements[this.currentElementIndex];
//   const textToSpeak = this.getElementText(element);

//   this.utterance = new SpeechSynthesisUtterance(textToSpeak);

//   // Sempre usar a voz feminina quando disponível
//   if (this.femaleVoice) {
//     this.utterance.voice = this.femaleVoice;
//   } else {
//     // Fallback para qualquer voz em português
//     const voices = this.speechSynth.getVoices();
//     const portugueseVoice = voices.find(v => v.lang.includes('pt'));
//     if (portugueseVoice) this.utterance.voice = portugueseVoice;
//   }

//   this.utterance.rate = this.speechRate;
//   this.utterance.pitch = 1.0;
//   this.utterance.lang = "pt-BR";

//   // Manter referência ao componente Vue no callback
//   const self = this;
  
//   this.utterance.onend = function() {
//     if (self.active && self.isPlaying) {
//       if (self.currentElementIndex < self.readableElements.length - 1) {
//         self.currentElementIndex++;
//         self.highlightCurrentElement();
//         self.updateReadingStatus();
//         self.speakCurrentElement();
//       } else {
//         self.isPlaying = false;
//         self.currentReadingStatus = "Leitura concluída";
//       }
//     }
//   };

//   this.utterance.onerror = function(event) {
//     console.error("Erro na síntese de fala:", event);
//     self.isPlaying = false;
//     self.currentReadingStatus = "Erro na leitura";
//   };

//   this.highlightCurrentElement();
//   this.speechSynth.speak(this.utterance);
//   this.isPlaying = true;
//   this.updateReadingStatus();
// },

pauseSpeaking() {
  if (this.speechSynth && this.speechSynth.speaking) {
    this.speechSynth.pause();
    this.isPlaying = false;
    this.currentReadingStatus = "Leitura pausada";
  }
},
    // Retoma a leitura pausada
    // resumeSpeaking() {
    //   if (this.speechSynth && this.speechSynth.paused) {
    //     this.speechSynth.resume();
    //     this.isPlaying = true;
    //     this.updateReadingStatus();
    //   }
    // },
   resumeSpeaking() {
  if (this.speechSynth && this.speechSynth.paused) {
    // Configura a voz antes de retomar
    this.setupVoice();
    this.speechSynth.resume();
    this.isPlaying = true;
    this.currentReadingStatus = "Retomando leitura";
  } else if (!this.speechSynth.speaking && !this.speechSynth.paused) {
    // Se não estava pausado, começa do atual
    this.startSpeakingFromCurrent();
  }
},
    // Para completamente a leitura
    // stopSpeaking() {
    //   if (this.speechSynth) {
    //     this.speechSynth.cancel();
    //     this.isPlaying = false;
    //   }
    // },
    stopSpeaking() {
  if (this.speechSynth) {
    this.speechSynth.cancel();
    this.isPlaying = false;
    // Limpa o utterance atual
    this.utterance = null;
  }
},
    removeAllHighlights() {
  // Remove destaques de elementos
  document.querySelectorAll(".sr-element-highlight").forEach((el) => {
    el.classList.remove("sr-element-highlight", "sr-interactive-indicator", "sr-container-indicator")
    
    // Remove tabindex temporário se foi adicionado
    if (el._tempTabindex) {
      el.removeAttribute('tabindex')
      delete el._tempTabindex
    }
  })

  // Remove destaques de palavras
  if (this.wordHighlightSpan) {
    const parent = this.wordHighlightSpan.parentNode
    if (parent) {
      parent.replaceChild(document.createTextNode(this.wordHighlightSpan.textContent), this.wordHighlightSpan)
      parent.normalize()
    }
    this.wordHighlightSpan = null
  }
},

    // Destaca visualmente o elemento atual
    highlightCurrentElement() {
  this.removeAllHighlights()

  if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
    const element = this.readableElements[this.currentElementIndex]
    
    element.classList.add("sr-element-highlight")
    
    // Adiciona indicador baseado no tipo de elemento
    if (this.isContainer(element) || this.hasExpandableContent(element)) {
      element.classList.add("sr-container-indicator")
    } else if (this.isInteractiveElement(element)) {
      element.classList.add("sr-interactive-indicator")
    }

    // Rola para o elemento e dá foco temporário
    element.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "nearest",
    })
    
    // Adiciona tabindex temporário se o elemento não for focável
    if (!element.hasAttribute('tabindex') && element.tabIndex === -1) {
      element.setAttribute('tabindex', '-1')
      element._tempTabindex = true
    }
    
    element.focus()
  }
},

    // Destaca visualmente a palavra atual
    highlightCurrentWord() {
      this.removeAllHighlights()

      if (this.currentElementIndex >= 0 && this.currentWordIndex >= 0 && 
          this.readableElements[this.currentElementIndex] && 
          this.currentWords[this.currentWordIndex]) {
        
        const element = this.readableElements[this.currentElementIndex]
        const word = this.currentWords[this.currentWordIndex]
        
        // Destaca o elemento pai também
        element.classList.add("sr-element-highlight")
        if (this.isContainer(element) || this.hasExpandableContent(element)) {
          element.classList.add("sr-container-indicator")
        } else if (this.isInteractiveElement(element)) {
          element.classList.add("sr-interactive-indicator")
        }
        
        // Encontra e destaca a palavra específica
        this.highlightWordInElement(element, word, this.currentWordIndex)

        element.scrollIntoView({
          behavior: "smooth",
          block: "center",
          inline: "nearest",
        })
      }
    },

    // Destaca uma palavra específica dentro de um elemento
    highlightWordInElement(element, targetWord, wordIndex) {
      const text = element.textContent
      const words = text.split(/(\s+)/)
      let actualWordIndex = 0
      
      // Cria um novo conteúdo com a palavra destacada
      const newContent = document.createDocumentFragment()
      
      words.forEach((segment) => {
        if (segment.trim().length > 0) {
          if (actualWordIndex === wordIndex && segment.trim() === targetWord.trim()) {
            const span = document.createElement('span')
            span.className = 'sr-word-highlight'
            span.textContent = segment
            this.wordHighlightSpan = span
            newContent.appendChild(span)
          } else {
            newContent.appendChild(document.createTextNode(segment))
          }
          actualWordIndex++
        } else {
          newContent.appendChild(document.createTextNode(segment))
        }
      })
      
      // Substitui o conteúdo do elemento
      element.innerHTML = ''
      element.appendChild(newContent)
    },

    // Função melhorada para atualizar status de leitura

    updateReadingStatus() {
  if (this.readableElements.length === 0) {
    this.currentReadingStatus = "Nenhum conteúdo para ler"
  } else if (this.currentElementIndex >= 0) {
    const element = this.readableElements[this.currentElementIndex]
    const elementText = this.getElementText(element)
    
    if (this.isAccordionButton(element)) {
      const targetId = element.getAttribute('data-bs-target') || 
                     element.getAttribute('aria-controls') || 
                     element.getAttribute('data-target')
      const selector = targetId?.startsWith('#') ? targetId : `#${targetId}`
      const target = selector ? document.querySelector(selector) : null
      
      // Verifica se o target realmente existe e está visível
      const isActuallyExpanded = target && target.classList.contains('show')
      const actualState = isActuallyExpanded ? 'expandido' : 'recolhido'
      
      this.currentReadingStatus = `Accordion ${actualState} - Enter para ${actualState === 'expandido' ? 'recolher' : 'expandir'}`
      this.announceForScreenReader(`${elementText}. ${actualState}. Pressione Enter para ${actualState === 'expandido' ? 'recolher' : 'expandir'}`)
    } else if (this.isContainer(element) || this.hasExpandableContent(element)) {
      this.currentReadingStatus = "Área expandível - Enter para entrar"
      this.announceForScreenReader(`${elementText}. Pressione Enter para expandir.`)
    } else if (this.isInteractiveElement(element)) {
      this.currentReadingStatus = "Elemento interativo - Enter para ativar"
      this.announceForScreenReader(`${elementText}. Pressione Enter para ativar.`)
    } else {
      this.currentReadingStatus = "A ler..."
    }
  } else {
    this.currentReadingStatus = this.isInContainer ? "Dentro de container" : "Leitor de ecrã ativo"
  }
},

    // Aumenta a velocidade de leitura
    increaseRate() {
      if (!this.speechSynth) return

      const currentRate = this.utterance ? this.utterance.rate : this.speechRate
      const newRate = Math.min(currentRate + 0.1, 2.0)

      if (this.utterance) {
        this.utterance.rate = newRate
      }

      this.speechRate = newRate

      const isKeyboardEvent = event && event.type === "keydown"
      if (isKeyboardEvent) {
        this.announceChange(`Velocidade: ${Math.round(newRate * 10) / 10}x`)
      }
    },

    // Exibe mensagem de confirmação temporária
    announceChange(message) {
      this.currentReadingStatus = message

      const notification = document.createElement("div")
      notification.style.cssText = `
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        z-index: 9999;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: sr-notification-slide 0.3s ease-out;
      `
      
      notification.textContent = message
      document.body.appendChild(notification)

      setTimeout(() => {
        if (document.body.contains(notification)) {
          notification.style.animation = 'sr-notification-slide 0.3s ease-out reverse'
          setTimeout(() => {
            if (document.body.contains(notification)) {
              document.body.removeChild(notification)
            }
          }, 300)
        }
        if (this.currentReadingStatus === message) {
          this.updateReadingStatus()
        }
      }, 2000)
    },

    announceForScreenReader(message) {
      // Só anuncia se não estiver reproduzindo já
      if (!this.isPlaying && this.speechSynth) {
        const utterance = new SpeechSynthesisUtterance(message)
        
        const voices = this.speechSynth.getVoices()
        const portugueseVoice = voices.find((voice) => voice.lang.includes("pt-BR") || voice.lang.includes("pt"))
        
        if (portugueseVoice) {
          utterance.voice = portugueseVoice
        }
        
        utterance.rate = this.speechRate
        utterance.pitch = 1.0
        utterance.lang = "pt-BR"
        utterance.volume = 0.8 // Um pouco mais baixo que a leitura normal
        
        // Cancela qualquer anúncio anterior e fala o novo
        this.speechSynth.cancel()
        this.speechSynth.speak(utterance)
      }
    },

    // Função melhorada para processar comandos de teclado
    handleKeyboardShortcuts(event) {
      if (!this.active || !this.isInitialized) return

      // Tratamento especial para Enter/Return no MacBook Air
      const isEnterKey = event.key === 'Enter' || event.key === 'Return' || event.keyCode === 13
      
      if (isEnterKey) {
        // Verifica se não está em um campo de input
        if (event.target.tagName !== 'INPUT' && 
            event.target.tagName !== 'TEXTAREA' && 
            !event.target.isContentEditable) {
          event.preventDefault()
          event.stopPropagation()
          this.activateElement()
        }
        return
      }

      switch (event.key) {
        case " ":
        case "Spacebar":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.playPause()
            event.preventDefault()
          }
          break
        case "p":
        case "P":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.playPause()
            event.preventDefault()
          }
          break
        case "ArrowRight":
        case "Right":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.nextElement()
            event.preventDefault()
          }
          break
        case "n":
        case "N":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.nextElement()
            event.preventDefault()
          }
          break
        case "ArrowLeft":
        case "Left":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.previousElement()
            event.preventDefault()
          }
          break
        case "b":
        case "B":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.previousElement()
            event.preventDefault()
          }
          break
        case "Home":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.restart()
            event.preventDefault()
          }
          break
        case "r":
        case "R":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.restart()
            event.preventDefault()
          }
          break
        case "w":
        case "W":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.setReadingMode(this.readingMode === 'word' ? 'element' : 'word')
            this.announceChange(`Modo: ${this.readingMode === 'word' ? 'Palavra' : 'Elemento'}`)
            event.preventDefault()
          }
          break
        case "Escape":
        case "Esc":
          if (this.isInContainer) {
            this.exitContainer()
          } else {
            this.stopSpeaking()
            this.$emit("update:screenReader", false)
          }
          event.preventDefault()
          break
        case "q":
        case "Q":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.stopSpeaking()
            this.$emit("update:screenReader", false)
            event.preventDefault()
          }
          break
        case "+":
        case "=":
          this.increaseRate()
          event.preventDefault()
          break
        case "-":
          this.decreaseRate()
          event.preventDefault()
          break
      }
    },
  },
}
</script>
