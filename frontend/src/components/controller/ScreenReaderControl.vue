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
        <!-- Controle de velocidade -->
        <div class="flex items-center justify-between mb-4">
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
              aria-label="Elemento anterior"
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
              {{ currentElementIndex >= 0 ? `${currentElementIndex + 1}/${readableElements.length}` : '0/0' }}
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
      currentReadingStatus: "Pronto para leitura",
      speechRate: 1.0,
      gatherTimeout: null,
      observer: null,
      pauseTimer: null,
      isInitialized: false,
      keysEnabled: false,
      navigationDebounce: null,
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
  },
  beforeUnmount() {
    this.cleanupReaderFeatures()
  },
  methods: {
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

    // Coleta elementos legíveis na página
    gatherReadableElements() {
      const mainContent = document.getElementById("main-content")
      if (!mainContent) {
        console.warn("Elemento #main-content não encontrado. Usando body como fallback.")
        const body = document.body

        const selector =
          'p, h1, h2, h3, h4, h5, h6, li, td, th, button:not([aria-hidden="true"]), a:not([aria-hidden="true"])'
        const allElements = body.querySelectorAll(selector)

        this.readableElements = Array.from(allElements).filter((el) => {
          const text = el.textContent.trim()
          const isVisible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
          const isInAccessibilityMenu = el.closest('[role="dialog"]') !== null
          const isPartOfReaderControl = el.closest(".screen-reader-control") !== null
          return text && isVisible && !isInAccessibilityMenu && !isPartOfReaderControl
        })
      } else {
        const selector =
          'p, h1, h2, h3, h4, h5, h6, li, td, th, button:not([aria-hidden="true"]), a:not([aria-hidden="true"])'
        const elements = mainContent.querySelectorAll(selector)

        this.readableElements = Array.from(elements).filter((el) => {
          const text = el.textContent.trim()
          const isVisible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
          return text && isVisible
        })
      }

      if (this.readableElements.length > 0) {
        this.currentReadingStatus = `${this.readableElements.length} elementos para ler`
      } else {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
      }
    },

    debounceGatherElements() {
      if (this.gatherTimeout) clearTimeout(this.gatherTimeout)
      this.gatherTimeout = setTimeout(() => {
        if (this.active) {
          this.gatherReadableElements()
        }
      }, 300)
    },

    // Iniciar/pausar a leitura
    playPause() {
      if (this.isPlaying) {
        this.pauseSpeaking()
      } else {
        if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
          this.currentElementIndex = 0
          this.highlightCurrentElement()
        }

        if (this.speechSynth && this.speechSynth.paused) {
          this.resumeSpeaking()
        } else {
          this.speakCurrentElement()
        }
      }
    },

    // Navega para o elemento anterior
    previousElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.currentElementIndex > 0) {
        this.currentElementIndex--
        this.highlightCurrentElement()
        this.updateReadingStatus()

        if (this.isPlaying) {
          setTimeout(() => {
            if (this.isPlaying) {
              this.speakCurrentElement()
            }
          }, 100)
        }
      }
    },

    // Navega para o próximo elemento
    nextElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.currentElementIndex < this.readableElements.length - 1) {
        this.currentElementIndex++
        this.highlightCurrentElement()
        this.updateReadingStatus()

        if (this.isPlaying) {
          setTimeout(() => {
            if (this.isPlaying) {
              this.speakCurrentElement()
            }
          }, 100)
        }
      }
    },

    // Reinicia a leitura do primeiro elemento
    restart() {
      this.stopSpeaking()

      if (this.readableElements.length > 0) {
        this.currentElementIndex = 0
        this.highlightCurrentElement()
        this.updateReadingStatus()

        if (this.isPlaying) {
          this.speakCurrentElement()
        }
      }
    },

    // Lê em voz alta o elemento atual
    speakCurrentElement() {
      if (
        !this.speechSynth ||
        this.currentElementIndex < 0 ||
        this.currentElementIndex >= this.readableElements.length
      ) {
        return
      }

      this.stopSpeaking()

      const currentElement = this.readableElements[this.currentElementIndex]
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

      this.utterance.onend = () => {
        if (this.active && this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++
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
        this.currentReadingStatus = "Leitura pausada"

        clearTimeout(this.pauseTimer)
        this.pauseTimer = setTimeout(() => {
          if (!this.isPlaying && this.speechSynth.paused) {
            this.speechSynth.resume()
            this.speechSynth.pause()
          }
        }, 5000)
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
      document.querySelectorAll(".reading-highlight").forEach((el) => {
        el.classList.remove("reading-highlight")
        el.style.outline = ""
      })
    },

    // Destaca visualmente o elemento atual
    highlightCurrentElement() {
      this.removeAllHighlights()

      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        element.classList.add("reading-highlight")
        element.style.outline = "3px solid #077b4b"

        element.scrollIntoView({
          behavior: "smooth",
          block: "center",
          inline: "nearest",
        })
      }
    },

    // Atualiza o status de leitura exibido
    updateReadingStatus() {
      if (this.readableElements.length === 0) {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
        return
      }

      if (this.currentElementIndex >= 0) {
        this.currentReadingStatus = `${this.currentElementIndex + 1} de ${this.readableElements.length}`
      } else {
        this.currentReadingStatus = `${this.readableElements.length} elementos para ler`
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
      notification.style.position = "fixed"
      notification.style.bottom = "80px"
      notification.style.left = "50%"
      notification.style.transform = "translateX(-50%)"
      notification.style.backgroundColor = "rgba(7, 123, 75, 0.8)"
      notification.style.color = "white"
      notification.style.padding = "10px 20px"
      notification.style.borderRadius = "20px"
      notification.style.zIndex = "9999"
      notification.textContent = message

      document.body.appendChild(notification)

      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification)
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
        case "Escape":
        case "Esc":
          this.stopSpeaking()
          this.$emit("update:active", false)
          event.preventDefault()
          break
        case "q":
        case "Q":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.stopSpeaking()
            this.$emit("update:active", false)
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

<style scoped>
/* Estilos para melhorar a aparência e acessibilidade */
button {
  transition: all 0.2s ease;
}

button:focus {
  outline: 2px solid #077b4b;
  outline-offset: 2px;
}

button:hover {
  transform: scale(1.05);
  opacity: 0.95;
}

/* Estilo para o elemento destacado na leitura */
:global(.reading-highlight) {
  transition: outline 0.3s ease;
}

/* Animação suave para transições */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>