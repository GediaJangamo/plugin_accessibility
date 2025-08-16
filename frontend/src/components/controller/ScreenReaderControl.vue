// VERSÃO DE DEBUGGING - Substitua TODO o componente por esta versão simplificada:

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
        <!-- Controle de velocidade -->
        <div class="flex items-center justify-center mb-4 gap-4">
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
              aria-label="Elemento anterior"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            
            <button 
              @click="activateElement"
              class="flex items-center justify-center bg-green-500 hover:bg-green-600 text-white p-3 rounded-lg shadow-sm transition-colors"
              aria-label="Ativar elemento atual (Enter)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7" />
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
              aria-label="Próximo elemento"
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

        <!-- Informações sobre navegação -->
        <div class="text-xs text-gray-500 dark:text-gray-400 text-center">
          <p>DEBUG: {{ debugInfo }}</p>
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
      currentReadingStatus: "Leitor inativo",
      speechRate: 1.0,
      isInitialized: false,
      keysEnabled: false,
      debugInfo: "Componente carregado - accordions devem funcionar",
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(newValue) {
        console.log('Screen Reader active changed:', newValue)
        if (newValue) {
          this.debugInfo = "Leitor ativado"
          this.$nextTick(() => {
            this.initReaderFeatures()
          })
        } else {
          this.debugInfo = "Leitor desativado - accordions devem funcionar"
          this.cleanupReaderFeatures()
        }
      },
    },
  },
  mounted() {
    console.log('Screen Reader component mounted')
    this.debugInfo = "Componente montado - sem interferência"
    // REMOVIDO TUDO que poderia interferir
  },
  beforeUnmount() {
    console.log('Screen Reader component beforeUnmount')
    this.cleanupReaderFeatures()
  },
  methods: {
    getProgressText() {
      if (this.readableElements.length > 0) {
        return this.currentElementIndex >= 0 ? `${this.currentElementIndex + 1}/${this.readableElements.length}` : '0/0'
      }
      return '0/0'
    },

    closeReader() {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.$emit('update:screenReader', false)
    },
    
    initReaderFeatures() {
      console.log('Initializing reader features')
      this.debugInfo = "Inicializando leitor..."
      
      this.initializeSpeechSynthesis()
      this.addCustomStyles()

      setTimeout(() => {
        this.gatherReadableElements()
        this.currentElementIndex = -1
        this.enableKeyboardControls()
        this.isInitialized = true
        this.debugInfo = `Leitor ativo - ${this.readableElements.length} elementos`
      }, 300)
    },

    cleanupReaderFeatures() {
      console.log('Cleaning up reader features')
      this.stopSpeaking()
      this.removeAllHighlights()
      this.disableKeyboardControls()
      this.removeCustomStyles()
      this.isInitialized = false
    },

    addCustomStyles() {
      if (!document.getElementById('screen-reader-highlight-styles')) {
        const style = document.createElement('style')
        style.id = 'screen-reader-highlight-styles'
        style.textContent = `
          .sr-element-highlight {
            outline: 2px solid rgba(59, 130, 246, 0.8) !important;
            outline-offset: 2px !important;
          }
        `
        document.head.appendChild(style)
      }
    },
    
    removeCustomStyles() {
      const style = document.getElementById('screen-reader-highlight-styles')
      if (style) {
        style.remove()
      }
    },

    enableKeyboardControls() {
      if (!this.keysEnabled) {
        document.addEventListener("keydown", this.handleKeyboardShortcuts)
        this.keysEnabled = true
      }
    },

    disableKeyboardControls() {
      document.removeEventListener("keydown", this.handleKeyboardShortcuts)
      this.keysEnabled = false
    },

    initializeSpeechSynthesis() {
      if ("speechSynthesis" in window) {
        this.speechSynth = window.speechSynthesis
        this.loadVoices()
      } else {
        this.currentReadingStatus = "Leitor não suportado"
      }
    },

    loadVoices() {
      if (this.speechSynth) {
        this.availableVoices = this.speechSynth.getVoices()
      }
    },

    gatherReadableElements() {
      // VERSÃO SUPER SIMPLES - sem interferir com accordions
      const mainContent = document.getElementById("main-content") || document.body
      
      const selector = 'h1, h2, h3, h4, h5, h6, p, a, button'
      const allElements = Array.from(mainContent.querySelectorAll(selector))
      
      this.readableElements = allElements.filter(el => {
        // Filtro MÍNIMO - só remove se realmente invisível
        const style = window.getComputedStyle(el)
        return style.display !== 'none' && style.visibility !== 'hidden'
      })

      this.currentReadingStatus = `${this.readableElements.length} elementos encontrados`
    },

    playPause() {
      if (this.isPlaying) {
        this.pauseSpeaking()
      } else {
        if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
          this.currentElementIndex = 0
          this.highlightCurrentElement()
        }
        this.speakCurrentElement()
      }
    },

    previousElement() {
      this.stopSpeaking()
      if (this.currentElementIndex > 0) {
        this.currentElementIndex--
      } else {
        this.currentElementIndex = this.readableElements.length - 1
      }
      this.highlightCurrentElement()
    },

    nextElement() {
      this.stopSpeaking()
      if (this.currentElementIndex < this.readableElements.length - 1) {
        this.currentElementIndex++
      } else {
        this.currentElementIndex = 0
      }
      this.highlightCurrentElement()
    },

    restart() {
      this.stopSpeaking()
      if (this.readableElements.length > 0) {
        this.currentElementIndex = 0
        this.highlightCurrentElement()
      }
    },

    speakCurrentElement() {
      if (!this.speechSynth || this.currentElementIndex < 0) return
      
      const currentElement = this.readableElements[this.currentElementIndex]
      const textToSpeak = currentElement.textContent.trim()

      this.utterance = new SpeechSynthesisUtterance(textToSpeak)
      this.utterance.rate = this.speechRate
      this.utterance.lang = "pt-BR"

      this.utterance.onend = () => {
        if (this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++
          this.highlightCurrentElement()
          setTimeout(() => this.speakCurrentElement(), 200)
        } else {
          this.isPlaying = false
          this.currentReadingStatus = "Leitura concluída"
        }
      }

      this.highlightCurrentElement()
      this.speechSynth.speak(this.utterance)
      this.isPlaying = true
    },

    pauseSpeaking() {
      if (this.speechSynth) {
        this.speechSynth.pause()
        this.isPlaying = false
      }
    },

    stopSpeaking() {
      if (this.speechSynth) {
        this.speechSynth.cancel()
        this.isPlaying = false
      }
    },

    removeAllHighlights() {
      document.querySelectorAll(".sr-element-highlight").forEach((el) => {
        el.classList.remove("sr-element-highlight")
      })
    },

    highlightCurrentElement() {
      this.removeAllHighlights()
      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        element.classList.add("sr-element-highlight")
        element.scrollIntoView({ behavior: "smooth", block: "center" })
      }
    },

    activateElement() {
      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        if (element.click) {
          element.click()
        }
      }
    },

    increaseRate() {
      this.speechRate = Math.min(this.speechRate + 0.1, 2.0)
    },

    decreaseRate() {
      this.speechRate = Math.max(this.speechRate - 0.1, 0.5)
    },

    handleKeyboardShortcuts(event) {
      if (!this.active || !this.isInitialized) return
      if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") return

      switch (event.key) {
        case " ":
        case "Spacebar":
          this.playPause()
          event.preventDefault()
          break
        case "ArrowRight":
          this.nextElement()
          event.preventDefault()
          break
        case "ArrowLeft":
          this.previousElement()
          event.preventDefault()
          break
        case "Enter":
          this.activateElement()
          event.preventDefault()
          break
        case "Escape":
          this.$emit("update:screenReader", false)
          event.preventDefault()
          break
      }
    },
  },
}
</script>