<template>
    <div 
      v-if="active"
      class="fixed bottom-5 left-1/2 transform -translate-x-1/2 bg-white dark:bg-gray-800 rounded-xl shadow-lg z-50 border border-gray-200 dark:border-gray-700 w-auto max-w-3xl transition-all duration-300 ease-in-out"
      aria-live="polite"
    >
      <div class="p-4">
        <!-- Status e informações -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center">
            <span class="text-gray-700 dark:text-gray-300 font-medium">{{ currentReadingStatus }}</span>
           
          </div>
          <div class="flex space-x-2">
            <!-- Botões de velocidade -->
            <div class="flex items-center bg-gray-100 dark:bg-gray-700 rounded-lg">
              <button 
                @click="decreaseRate"
                class="flex items-center justify-center text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white p-1.5 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
                aria-label="Diminuir velocidade"
                title="Diminuir velocidade"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                </svg>
              </button>
              <span class="px-2 text-sm p-4 bg-[#077b4b] text-white dark:text-gray-300">{{ speechRate.toFixed(1) }}x</span>
              <button 
                @click="increaseRate"
                class="flex items-center justify-center text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white p-1.5 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
                aria-label="Aumentar velocidade"
                title="Aumentar velocidade"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Controles principais -->
        <div class="flex items-center justify-between gap-3">
          <!-- Botão principal de play/pause -->
          <button 
            @click="playPause"
            class="flex items-center justify-center bg-[#077b4b] hover:bg-green-600 text-white p-4 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-md transition-all duration-200 transform hover:scale-105"
            :aria-label="isPlaying ? 'Pausar leitura' : 'Iniciar leitura'"
            title="Iniciar/Pausar leitura"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path v-if="!isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path v-if="isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          
          <!-- Grupo de controles de navegação -->
          <div class="flex items-center justify-center space-x-2 bg-gray-100 dark:bg-gray-700 p-2 rounded-xl flex-1">
            <button 
              @click="previousElement"
              class="flex items-center justify-center bg-white hover:bg-gray-200 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-white p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors shadow-sm"
              aria-label="Elemento anterior"
              title="Elemento anterior"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#077b4b] " fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            
            <button 
              @click="restart"
              class="flex items-center justify-center bg-white hover:bg-gray-200 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-white p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors shadow-sm"
              aria-label="Reiniciar leitura"
              title="Reiniciar leitura"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500 " fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            
            <button 
              @click="nextElement"
              class="flex items-center justify-center bg-white hover:bg-gray-200 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-white p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors shadow-sm"
              aria-label="Próximo elemento"
              title="Próximo elemento"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#077b4b]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          
          <!-- Indicador de progresso -->
          <div class="bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-lg text-center min-w-[80px]">
            <span class="text-gray-700 dark:text-gray-300 text-sm font-medium">
              {{ currentElementIndex >= 0 ? `${currentElementIndex + 1}/${readableElements.length}` : '0/0' }}
            </span>
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
      isInitialized: false, // Controle de inicialização
      keysEnabled: false, // Controle para ativação dos comandos de teclado
      navigationDebounce: null, // Debounce para navegação de teclado
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
    // Observa mudanças no DOM quando o componente é montado
    this.initMutationObserver()
  },
  beforeUnmount() {
    this.cleanupReaderFeatures()
  },
  methods: {
    // Inicializa todos os recursos do leitor
    initReaderFeatures() {
      this.initializeSpeechSynthesis()

      // Define um pequeno atraso para garantir que o DOM esteja pronto
      setTimeout(() => {
        this.gatherReadableElements()

        // Não destacar nenhum elemento até que o usuário inicie a leitura
        this.currentElementIndex = -1
        this.removeAllHighlights()

        // Adiciona os event listeners de teclado
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

        // Carrega as vozes disponíveis quando estiverem prontas
        if (this.speechSynth.onvoiceschanged !== undefined) {
          this.speechSynth.onvoiceschanged = this.loadVoices
        }

        // Tenta carregar vozes imediatamente
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
      // Seleciona apenas elementos dentro do conteúdo principal
      const mainContent = document.getElementById("main-content")
      if (!mainContent) {
        console.warn("Elemento #main-content não encontrado. Usando body como fallback.")
        // Se não encontrar o main-content, usa o body inteiro exceto o menu de acessibilidade
        const body = document.body

        // Seleciona elementos de texto com conteúdo visível
        const selector =
          'p, h1, h2, h3, h4, h5, h6, li, td, th, button:not([aria-hidden="true"]), a:not([aria-hidden="true"])'
        const allElements = body.querySelectorAll(selector)

        // Exclui elementos do menu de acessibilidade
        this.readableElements = Array.from(allElements).filter((el) => {
          // Filtra elementos vazios ou ocultos ou dentro do menu de acessibilidade
          const text = el.textContent.trim()
          const isVisible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
          const isInAccessibilityMenu = el.closest('[role="dialog"]') !== null
          const isPartOfReaderControl = el.closest(".screen-reader-control") !== null
          return text && isVisible && !isInAccessibilityMenu && !isPartOfReaderControl
        })
      } else {
        // Código original para quando o main-content existe
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
        // Se não tiver elemento atual selecionado, comece pelo primeiro
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
      // Evita navegação rápida demais através de debounce
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
          // Pequeno delay para dar tempo ao usuário de perceber a mudança
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
      // Evita navegação rápida demais através de debounce
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
          // Pequeno delay para dar tempo ao usuário de perceber a mudança
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

      // Cancela qualquer fala anterior
      this.stopSpeaking()

      const currentElement = this.readableElements[this.currentElementIndex]
      const textToSpeak = currentElement.textContent.trim()

      this.utterance = new SpeechSynthesisUtterance(textToSpeak)

      // Tenta definir a voz em português do Brasil, se disponível
      const voices = this.speechSynth.getVoices()
      const portugueseVoice = voices.find((voice) => voice.lang.includes("pt-BR") || voice.lang.includes("pt"))

      if (portugueseVoice) {
        this.utterance.voice = portugueseVoice
      }

      this.utterance.rate = this.speechRate
      this.utterance.pitch = 1.0
      this.utterance.lang = "pt-BR"

      this.utterance.onend = () => {
        // Verifica se ainda está ativo e se há mais elementos
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

        // Alguns navegadores podem ter problemas com pause/resume
        // Então adiciona um temporizador para evitar que a síntese trave
        clearTimeout(this.pauseTimer)
        this.pauseTimer = setTimeout(() => {
          if (!this.isPlaying && this.speechSynth.paused) {
            // Força retomada se ficar pausado por muito tempo
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
      // Remove destaque anterior
      this.removeAllHighlights()

      // Adiciona novo destaque
      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        element.classList.add("reading-highlight")
        element.style.outline = "3px solid #077b4b" // Borda verde mais espessa

        // Garante que o elemento seja visível na tela
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
      const newRate = Math.min(currentRate + 0.1, 2.0) // Máximo de 2x

      // Atualiza a taxa para o utterance atual
      if (this.utterance) {
        this.utterance.rate = newRate
      }

      // Armazena a nova taxa para futuros utterances
      this.speechRate = newRate

      // Anuncia a mudança APENAS se for via teclado
      const isKeyboardEvent = event && event.type === "keydown"
      if (isKeyboardEvent) {
        this.announceChange(`Velocidade: ${Math.round(newRate * 10) / 10}x`)
      }
    },

    // Diminui a velocidade de leitura
    decreaseRate() {
      if (!this.speechSynth) return

      const currentRate = this.utterance ? this.utterance.rate : this.speechRate
      const newRate = Math.max(currentRate - 0.1, 0.5) // Mínimo de 0.5x

      // Atualiza a taxa para o utterance atual
      if (this.utterance) {
        this.utterance.rate = newRate
      }

      // Armazena a nova taxa para futuros utterances
      this.speechRate = newRate

      // Anuncia a mudança APENAS se for via teclado
      const isKeyboardEvent = event && event.type === "keydown"
      if (isKeyboardEvent) {
        this.announceChange(`Velocidade: ${Math.round(newRate * 10) / 10}x`)
      }
    },

    // Exibe mensagem de confirmação temporária
    announceChange(message) {
      // Armazena o status atual para restaurar depois
      //const originalStatus = this.currentReadingStatus;
      this.currentReadingStatus = message

      // Criar uma notificação temporária para usuários com visão
      const notification = document.createElement("div")
      notification.style.position = "fixed"
      notification.style.bottom = "80px"
      notification.style.left = "50%"
      notification.style.transform = "translateX(-50%)"
      notification.style.backgroundColor = "rgba(7, 123, 75, 0.8)" // Cor verde do sistema
      notification.style.color = "white"
      notification.style.padding = "10px 20px"
      notification.style.borderRadius = "20px"
      notification.style.zIndex = "9999"
      notification.textContent = message

      document.body.appendChild(notification)

      // Restaura o status original após um tempo
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification)
        }
        // Não restaura o status se ele foi alterado por outra operação
        if (this.currentReadingStatus === message) {
          this.updateReadingStatus()
        }
      }, 2000)
    },

    // Processa comandos de teclado
    handleKeyboardShortcuts(event) {
      // Só processa atalhos quando o componente está ativo
      if (!this.active || !this.isInitialized) return

      // Verifica se o foco não está em um campo de entrada, área de texto ou elemento editável
      if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA" || event.target.isContentEditable) {
        return // Não intercepta teclas em campos de entrada
      }

      switch (event.key) {
        // Play/Pause - Espaço ou P
        case " ":
        case "Spacebar": // Para alguns navegadores mais antigos
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

        // Próximo elemento - Seta direita ou N
        case "ArrowRight":
        case "Right": // Para navegadores mais antigos
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

        // Elemento anterior - Seta esquerda ou B
        case "ArrowLeft":
        case "Left": // Para navegadores mais antigos
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

        // Reiniciar - Home ou R
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

        // Parar/Fechar - Escape ou Q
        case "Escape":
        case "Esc": // Para navegadores mais antigos
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

        // Controle de velocidade
        case "+":
        case "=": // Mesmo botão no teclado americano
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