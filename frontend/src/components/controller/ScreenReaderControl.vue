<template>
  <div 
    v-if="active"
    class="fixed bottom-5 left-1/2 transform -translate-x-1/2 z-50 transition-all duration-300 ease-in-out"
    aria-live="polite"
  >
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden w-auto max-w-3xl">
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
        <div class="flex items-center gap-4">
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
      processedAccordions: new Set(),
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
    this.initMutationObserver()
    this.addCustomStyles()
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
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 197, 253, 0.15)) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4), 0 0 20px rgba(59, 130, 246, 0.3) !important;
            transform: scale(1.02) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            z-index: 10 !important;
          }
          
          .sr-element-highlight::before {
            content: '' !important;
            position: absolute !important;
            top: -4px !important;
            left: -4px !important;
            right: -4px !important;
            bottom: -4px !important;
            background: linear-gradient(45deg, #3b82f6, #06b6d4) !important;
            border-radius: 12px !important;
            z-index: -1 !important;
            opacity: 0.6 !important;
            filter: blur(8px) !important;
            animation: sr-glow-pulse 2s ease-in-out infinite alternate !important;
          }
          
          .sr-word-highlight {
            background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
            color: white !important;
            padding: 2px 4px !important;
            border-radius: 4px !important;
            box-shadow: 0 2px 8px #3b82f6 !important;
            transform: scale(1.05) !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
          }
          
          @keyframes sr-glow-pulse {
            0% { opacity: 0.4; transform: scale(1); }
            100% { opacity: 0.8; transform: scale(1.01); }
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
        const text = element.textContent.trim()
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
      this.$emit('update:screenReader', false);
    },
    
    // Inicializa todos os recursos do leitor
    initReaderFeatures() {
      this.initializeSpeechSynthesis()

      setTimeout(() => {
        this.gatherReadableElements()
        this.currentElementIndex = -1
        this.removeAllHighlights()
        this.enableKeyboardControls()
        this.isInitialized = true
      }, 300)
    },

    // Limpa todos os recursos do leitor
    cleanupReaderFeatures() {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.disableKeyboardControls()

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

    loadVoices() {
      if (this.speechSynth) {
        this.availableVoices = this.speechSynth.getVoices()
      }
    },

    // Função melhorada para abrir accordions automaticamente
    expandAccordionForElement(element) {
      let current = element
      while (current && current !== document.body) {
        // Verifica se está dentro de um accordion fechado
        const accordionCollapse = current.closest('.accordion-collapse.collapse:not(.show)')
        if (accordionCollapse) {
          const targetId = accordionCollapse.id
          const trigger = document.querySelector(`[data-bs-target="#${targetId}"]`)
          
          if (trigger && !accordionCollapse.classList.contains('show')) {
            // Simula um clique no botão do accordion
            trigger.click()
            
            // Aguarda a animação de abertura
            return new Promise(resolve => {
              setTimeout(() => {
                resolve()
              }, 350) // Tempo da animação do Bootstrap
            })
          }
        }
        current = current.parentElement
      }
      return Promise.resolve()
    },

    // Coleta elementos que podem ser lidos, incluindo os em accordions
    async gatherReadableElements() {
      const mainContent = document.getElementById("main-content") || document.body
      
      // Seletor mais específico para evitar duplicatas
      const selector = `

      img:not(.sr-skip),
      svg[aria-label]:not(.sr-skip),
      h1:not(.sr-skip),
      h2:not(.sr-skip),
      h3:not(.sr-skip),
      h4:not(.sr-skip),
      h5:not(.sr-skip),
      h6:not(.sr-skip),
      .course-header h6,
      .accordion-button,
      p:not(.sr-skip),
      a:not([aria-hidden="true"]):not(.sr-skip),,
      span:not(.sr-skip):not(.text-muted),
      li:not(.sr-skip),
      td:not(.sr-skip),
      th:not(.sr-skip),
      button:not(.sr-skip),
      label:not(.sr-skip),
      input[aria-label]:not(.sr-skip),
      textarea[aria-label]:not(.sr-skip)

      `
      
      // Primeiro, encontra todos os elementos, incluindo os em accordions fechados
      const allElements = mainContent.querySelectorAll(selector)
      
      this.readableElements = Array.from(allElements).filter((el) => {
        let text = "";

        if (el.tagName.toLowerCase() === "img") {
            text = el.alt?.trim() || "";
        } else if (el.tagName.toLowerCase() === "svg") {
            text = el.getAttribute("aria-label")?.trim() || "";
        } else {
            text = el.textContent.trim();
        }

        if (!text || text.length < 1) return false;
        
        // Ignora elementos do próprio leitor de tela
        if (el.closest('.screen-reader-control') || el.closest('[data-screen-reader-ignore]')) {
          return false
        }
        
        // Ignora elementos com classes específicas que não devem ser lidos
        if (el.classList.contains('text-muted') && el.tagName.toLowerCase() !== 'small') {
          return false
        }
        
        // Verifica se é um elemento duplicado (mesmo texto no mesmo contexto)
        const parent = el.closest('.course-item, .accordion-item')
        if (parent) {
          const siblings = parent.querySelectorAll(el.tagName.toLowerCase())
          const sameTextSiblings = Array.from(siblings).filter(sibling => 
            sibling.textContent.trim() === text && sibling !== el
          )
          if (sameTextSiblings.length > 0 && Array.from(siblings).indexOf(el) > 0) {
            return false
          }
        }
        
        return true
      })

      // Remove elementos duplicados baseado no conteúdo e posição
      this.readableElements = this.removeDuplicateElements(this.readableElements)

      if (this.readableElements.length > 0) {
        this.currentReadingStatus = "Leitor de ecrã activo"
      } else {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
      }
    },

    // Remove elementos duplicados
    removeDuplicateElements(elements) {
      const seen = new Map()
      
      return elements.filter(el => {
        const text = el.textContent.trim().toLowerCase()
        const tag = el.tagName.toLowerCase()
        const key = `${tag}:${text}`
        
        // Para elementos muito pequenos ou comuns, é mais restritivo
        if (text.length < 10 || ['sim', 'não', 'ok', 'cancelar'].includes(text)) {
          const rect = el.getBoundingClientRect()
          const positionKey = `${key}:${Math.round(rect.top)}:${Math.round(rect.left)}`
          
          if (seen.has(positionKey)) {
            return false
          }
          seen.set(positionKey, true)
          return true
        }
        
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
        if (this.active) {
          this.gatherReadableElements()
        }
      }, 500) // Aumentado para evitar muitas atualizações
    },

    // Iniciar/pausar a leitura
    playPause() {
      if (this.isPlaying) {
        this.pauseSpeaking()
      } else {
        if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
          this.currentElementIndex = 0
          if (this.readingMode === 'word') {
            this.setupWordReading()
          } else {
            this.highlightCurrentElement()
          }
        }

        if (this.speechSynth && this.speechSynth.paused) {
          this.resumeSpeaking()
        } else {
          this.speakCurrent()
        }
      }
    },

    // Navega para o elemento/palavra anterior
    previousElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.readingMode === 'word') {
        if (this.currentWordIndex > 0) {
          this.currentWordIndex--
          this.highlightCurrentWord()
        } else if (this.currentElementIndex > 0) {
          this.currentElementIndex--
          this.setupWordReading()
        }
      } else {
        if (this.currentElementIndex > 0) {
          this.currentElementIndex--
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
    async speakCurrent() {
      if (this.readingMode === 'word') {
        await this.speakCurrentWord()
      } else {
        await this.speakCurrentElement()
      }
    },

    // Lê em voz alta a palavra atual
    async speakCurrentWord() {
      if (!this.speechSynth || this.currentWordIndex < 0 || this.currentWordIndex >= this.currentWords.length) {
        return
      }

      this.stopSpeaking()

      const word = this.currentWords[this.currentWordIndex]
      this.utterance = new SpeechSynthesisUtterance(word)

      const voices = this.speechSynth.getVoices()
      const portugueseVoice = voices.find((voice) => voice.lang.includes("pt-BR") || voice.lang.includes("pt"))

      if (portugueseVoice) {
        this.utterance.voice = portugueseVoice
      }

      this.utterance.rate = this.speechRate
      this.utterance.pitch = 1.0
      this.utterance.lang = "pt-BR"

      this.utterance.onend = async () => {
        if (this.active) {
          if (this.currentWordIndex < this.currentWords.length - 1) {
            this.currentWordIndex++
            this.highlightCurrentWord()
            this.updateReadingStatus()
            this.speakCurrentWord()
          } else if (this.currentElementIndex < this.readableElements.length - 1) {
            this.currentElementIndex++
            await this.expandAccordionForElement(this.readableElements[this.currentElementIndex])
            this.setupWordReading()
            this.updateReadingStatus()
            this.speakCurrentWord()
          } else {
            this.isPlaying = false
            this.currentReadingStatus = "Leitura concluída"
          }
        }
      }

      this.utterance.onerror = (event) => {
        console.error("Erro na síntese de fala:", event)
        this.isPlaying = false
        this.currentReadingStatus = "Erro na leitura"
      }

      this.highlightCurrentWord()
      this.speechSynth.speak(this.utterance)
      this.isPlaying = true
      this.updateReadingStatus()
    },

    // Lê em voz alta o elemento atual
    async speakCurrentElement() {
      if (
        !this.speechSynth ||
        this.currentElementIndex < 0 ||
        this.currentElementIndex >= this.readableElements.length
      ) {
        return
      }

      this.stopSpeaking()

      const currentElement = this.readableElements[this.currentElementIndex]
      
      // Expande accordion se necessário antes de ler
      await this.expandAccordionForElement(currentElement)
      
      const textToSpeak = currentElement.textContent.trim()

      this.utterance = new SpeechSynthesisUtterance(textToSpeak)

      const voices = this.speechSynth.getVoices()
      const portugueseVoice = voices.find((voice) => voice.lang.includes("pt-BR") || voice.lang.includes("pt"))

      if (portugueseVoice) {
        this.utterance.voice = portugueseVoice
      }

      this.utterance.rate = this.speechRate
      this.utterance.pitch = 1.0
      this.utterance.lang = "pt-BR"

      this.utterance.onend = async () => {
        if (this.active && this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++
          await this.expandAccordionForElement(this.readableElements[this.currentElementIndex])
          this.highlightCurrentElement()
          this.updateReadingStatus()
          this.speakCurrentElement()
        } else {
          this.isPlaying = false
          this.currentReadingStatus = "Leitura concluída"
        }
      }

      this.utterance.onerror = (event) => {
        console.error("Erro na síntese de fala:", event)
        this.isPlaying = false
        this.currentReadingStatus = "Erro na leitura"
      }

      this.highlightCurrentElement()
      this.speechSynth.speak(this.utterance)
      this.isPlaying = true
      this.updateReadingStatus()
    },

    // Pausa a leitura em andamento
    pauseSpeaking() {
      if (this.speechSynth && this.isPlaying) {
        this.speechSynth.pause()
        this.isPlaying = false
      }
    },

    // Retoma a leitura pausada
    resumeSpeaking() {
      if (this.speechSynth && this.speechSynth.paused) {
        clearTimeout(this.pauseTimer)
        this.speechSynth.resume()
        this.isPlaying = true
        this.updateReadingStatus()
      }
    },

    // Para completamente a leitura
    stopSpeaking() {
      if (this.speechSynth) {
        this.speechSynth.cancel()
        this.isPlaying = false
      }
    },

    // Remove todos os destaques visuais
    removeAllHighlights() {
      // Remove destaques de elementos
      document.querySelectorAll(".sr-element-highlight").forEach((el) => {
        el.classList.remove("sr-element-highlight")
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
    async highlightCurrentElement() {
      this.removeAllHighlights()

      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        
        // Expande accordion se necessário
        await this.expandAccordionForElement(element)
        
        element.classList.add("sr-element-highlight")

        element.scrollIntoView({
          behavior: "smooth",
          block: "center",
          inline: "nearest",
        })
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

    updateReadingStatus() {
      if (this.readableElements.length === 0) {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
      } else {
        this.currentReadingStatus = "Leitor de ecrã activo"
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

    // Diminui a velocidade de leitura
    decreaseRate() {
      if (!this.speechSynth) return

      const currentRate = this.utterance ? this.utterance.rate : this.speechRate
      const newRate = Math.max(currentRate - 0.1, 0.5)

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
        box-shadow: 0 4px 20px #3b82f6;
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

    // Processa comandos de teclado
    handleKeyboardShortcuts(event) {
      if (!this.active || !this.isInitialized) return

      if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA" || event.target.isContentEditable) {
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
          this.stopSpeaking()
          this.$emit("update:screenReader", false)
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