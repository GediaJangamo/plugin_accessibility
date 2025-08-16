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
          <p>Navegação: ← → ou B/N • Ativar: Enter • Play/Pause: Espaço/P • Sair: Esc/Q</p>
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
    addCustomStyles() {
      if (!document.getElementById('screen-reader-highlight-styles')) {
        const style = document.createElement('style')
        style.id = 'screen-reader-highlight-styles'
        style.textContent = `
          .sr-element-highlight {
            outline: 2px solid rgba(59, 130, 246, 0.8) !important;
            outline-offset: 2px !important;
            background-color: rgba(59, 130, 246, 0.1) !important;
          }
          
          @keyframes sr-notification-slide {
            from { transform: translateX(-50%) translateY(20px); opacity: 0; }
            to { transform: translateX(-50%) translateY(0); opacity: 1; }
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
      this.initializeSpeechSynthesis()

      setTimeout(() => {
        this.gatherReadableElements()
        this.currentElementIndex = -1
        this.removeAllHighlights()
        this.enableKeyboardControls()
        this.isInitialized = true
      }, 300)
    },

    cleanupReaderFeatures() {
      this.stopSpeaking()
      this.removeAllHighlights()
      this.disableKeyboardControls()

      if (this.observer) {
        this.observer.disconnect()
      }

      this.isInitialized = false
    },

    // initMutationObserver() {
    //   if (window.MutationObserver) {
    //     this.observer = new MutationObserver(this.debounceGatherElements)
    //     this.observer.observe(document.body, {
    //       childList: true,
    //       subtree: true,
    //       attributes: true,
    //       attributeFilter: ['class', 'style', 'aria-expanded', 'hidden']
    //     })
    //   }
    // },
    initMutationObserver() {
  if (window.MutationObserver) {
    this.observer = new MutationObserver((mutations) => {
      let shouldUpdate = false
      
      mutations.forEach((mutation) => {
        // Detecta mudanças em classes (como 'show' sendo adicionada/removida)
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          const target = mutation.target
          if (target.classList.contains('accordion-collapse') || target.classList.contains('collapse')) {
            shouldUpdate = true
          }
        }
        
        // Detecta mudanças na estrutura DOM
        if (mutation.type === 'childList') {
          shouldUpdate = true
        }
      })
      
      if (shouldUpdate) {
        this.debounceGatherElements()
      }
    })
    
    this.observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['class', 'style', 'aria-expanded', 'hidden']
    })
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

    getElementText(element) {
      const tag = element.tagName.toLowerCase()
      
      // Para accordion buttons
      if (this.isAccordionButton(element)) {
        const isExpanded = element.getAttribute('aria-expanded') === 'true'
        const text = element.textContent.trim()
        return `Botão de accordion ${isExpanded ? 'expandido' : 'recolhido'}: ${text}. Pressione Enter para ${isExpanded ? 'recolher' : 'expandir'}`
      }
      
      // Para imagens
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
      
      // Para SVGs
      if (tag === 'svg') {
        return element.getAttribute('aria-label') || 'Gráfico sem descrição'
      }
      
      // Para elementos interativos, adiciona contexto
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

      // Para cabeçalhos, adiciona o nível
      if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tag)) {
        const level = tag.charAt(1)
        return `Cabeçalho nível ${level}: ${element.textContent.trim()}`
      }
      
      return element.textContent.trim()
    },

    isAccordionButton(element) {
      return element.classList.contains('accordion-button') || 
             (element.hasAttribute('data-bs-toggle') && element.getAttribute('data-bs-toggle') === 'collapse')
    },

    async gatherReadableElements() {
      const mainContent = document.getElementById("main-content") || document.body
      
      const selector = `
        h1, h2, h3, h4, h5, h6,
        p,
        a:not([aria-hidden="true"]),
        button,
        input[type="text"], input[type="email"], input[type="password"], input[type="search"],
        textarea,
        select,
        label,
        li,
        td,
        th,
        img,
        svg[aria-label],
        .accordion-button,
        [data-bs-toggle="collapse"]
      `
      
      const allElements = Array.from(mainContent.querySelectorAll(selector))
      
      this.readableElements = allElements.filter(el => {
        if (el.closest('.screen-reader-control') || el.closest('[data-screen-reader-ignore]')) {
          return false
        }
        
        if (!this.isElementVisible(el)) {
          return false
        }
        
        const text = this.getElementText(el)
        return text && text.trim().length > 0
      }).sort((a, b) => {
        const rectA = a.getBoundingClientRect()
        const rectB = b.getBoundingClientRect()
        
        if (Math.abs(rectA.top - rectB.top) > 10) {
          return rectA.top - rectB.top
        }
        return rectA.left - rectB.left
      })

      this.readableElements = this.removeDuplicateElements(this.readableElements)

      if (this.readableElements.length > 0) {
        this.currentReadingStatus = `${this.readableElements.length} elementos encontrados`
      } else {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
      }
    },

    // isElementVisible(element) {
    //   const style = window.getComputedStyle(element)
    //   if (style.display === 'none' || style.visibility === 'hidden' || element.hasAttribute('hidden')) {
    //     return false
    //   }
      
    //   let parent = element.parentElement
    //   while (parent && parent !== document.body) {
    //     if (parent.classList.contains('accordion-collapse') && 
    //         !parent.classList.contains('show')) {
    //       return false
    //     }
    //     parent = parent.parentElement
    //   }
      
    //   return true
    // },

    isElementVisible(element) {
  // Verificações básicas de CSS
  const style = window.getComputedStyle(element)
  if (style.display === 'none' || style.visibility === 'hidden' || element.hasAttribute('hidden')) {
    return false
  }
  
  // Para accordions Bootstrap, verificamos se o elemento está dentro de um collapse
  let currentElement = element
  while (currentElement && currentElement !== document.body) {
    // Se o elemento está dentro de um accordion-collapse
    if (currentElement.classList.contains('accordion-collapse')) {
      // Verifica se tem a classe 'show' (expandido) ou 'collapse' (recolhido)
      const isExpanded = currentElement.classList.contains('show')
      return isExpanded
    }
    
    // Para outros tipos de collapse do Bootstrap
    if (currentElement.classList.contains('collapse') && !currentElement.classList.contains('accordion-collapse')) {
      const isExpanded = currentElement.classList.contains('show')
      return isExpanded
    }
    
    currentElement = currentElement.parentElement
  }
  
  // Verificação de visibilidade no viewport (opcional, mas útil)
  const rect = element.getBoundingClientRect()
  if (rect.width === 0 && rect.height === 0) {
    return false
  }
  
  return true
},

handleAccordionInteraction(element) {
  const isExpanded = element.getAttribute('aria-expanded') === 'true'
  
  this.announceChange(isExpanded ? 'Recolhendo accordion...' : 'Expandindo accordion...')
  
  element.click()
  
  // Aumentamos o timeout para dar tempo ao Bootstrap processar a animação
  setTimeout(() => {
    // Força uma re-detecção completa
    this.gatherReadableElements()
    
    if (!isExpanded) {
      // Se expandiu, tenta encontrar o primeiro elemento dentro do accordion
      const targetId = element.getAttribute('data-bs-target') || 
                      element.getAttribute('aria-controls')
      if (targetId) {
        const targetElement = document.querySelector(targetId)
        if (targetElement) {
          // Aguarda um pouco mais para a animação terminar
          setTimeout(() => {
            const firstChildElement = this.findFirstReadableChild(targetElement)
            if (firstChildElement) {
              const newIndex = this.readableElements.indexOf(firstChildElement)
              if (newIndex !== -1) {
                this.currentElementIndex = newIndex
                this.highlightCurrentElement()
              }
            }
          }, 200) // Timeout adicional para animação
        }
      }
    }
    
    this.announceChange(`Accordion ${isExpanded ? 'recolhido' : 'expandido'}`)
  }, 800) // Aumentado de 500ms para 800ms
},

    removeDuplicateElements(elements) {
      const seen = new Map()
      
      return elements.filter(el => {
        const text = this.getElementText(el).toLowerCase().trim()
        const tag = el.tagName.toLowerCase()
        
        if (tag === 'img') {
          const key = `${tag}:${text}:${el.src}`
          if (seen.has(key)) return false
          seen.set(key, true)
          return true
        }
        
        const key = `${tag}:${text}`
        
        if (seen.has(key)) {
          const rect = el.getBoundingClientRect()
          const seenData = seen.get(key)
          
          if (seenData && Math.abs(seenData.top - rect.top) < 5 && Math.abs(seenData.left - rect.left) < 5) {
            return false
          }
        }
        
        const rect = el.getBoundingClientRect()
        seen.set(key, { top: rect.top, left: rect.left })
        return true
      })
    },

    debounceGatherElements() {
      if (this.gatherTimeout) clearTimeout(this.gatherTimeout)
      this.gatherTimeout = setTimeout(() => {
        if (this.active) {
          this.gatherReadableElements()
        }
      }, 500)
    },

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

    previousElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.currentElementIndex > 0) {
        this.currentElementIndex--
      } else {
        this.currentElementIndex = this.readableElements.length - 1
      }

      this.highlightCurrentElement()
      this.updateReadingStatus()

      if (this.isPlaying) {
        setTimeout(() => {
          if (this.isPlaying) {
            this.speakCurrentElement()
          }
        }, 100)
      }
    },

    nextElement() {
      if (this.navigationDebounce) return
      this.navigationDebounce = setTimeout(() => {
        this.navigationDebounce = null
      }, 200)

      this.stopSpeaking()

      if (this.currentElementIndex < this.readableElements.length - 1) {
        this.currentElementIndex++
      } else {
        this.currentElementIndex = 0
      }

      this.highlightCurrentElement()
      this.updateReadingStatus()

      if (this.isPlaying) {
        setTimeout(() => {
          if (this.isPlaying) {
            this.speakCurrentElement()
          }
        }, 100)
      }
    },

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
      const textToSpeak = this.getElementText(currentElement)

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
          this.highlightCurrentElement()
          this.updateReadingStatus()
          setTimeout(() => {
            this.speakCurrentElement()
          }, 200)
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

    pauseSpeaking() {
      if (this.speechSynth && this.isPlaying) {
        this.speechSynth.pause()
        this.isPlaying = false
      }
    },

    resumeSpeaking() {
      if (this.speechSynth && this.speechSynth.paused) {
        clearTimeout(this.pauseTimer)
        this.speechSynth.resume()
        this.isPlaying = true
        this.updateReadingStatus()
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

    async highlightCurrentElement() {
      this.removeAllHighlights()

      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        
        element.classList.add("sr-element-highlight")

        element.scrollIntoView({
          behavior: "smooth",
          block: "center",
          inline: "nearest",
        })
      }
    },

    updateReadingStatus() {
      if (this.readableElements.length === 0) {
        this.currentReadingStatus = "Nenhum conteúdo para ler"
      } else if (this.currentElementIndex >= 0) {
        const element = this.readableElements[this.currentElementIndex]
        const elementType = this.getElementType(element)
        this.currentReadingStatus = `${elementType} (${this.currentElementIndex + 1}/${this.readableElements.length})`
      } else {
        this.currentReadingStatus = "Leitor de tela ativo"
      }
    },

    getElementType(element) {
      const tag = element.tagName.toLowerCase()
      
      if (this.isAccordionButton(element)) return 'Accordion'
      if (tag === 'button') return 'Botão'
      if (tag === 'a') return 'Link'
      if (tag.startsWith('h')) return 'Cabeçalho'
      if (tag === 'img') return 'Imagem'
      if (tag === 'p') return 'Parágrafo'
      if (tag === 'li') return 'Item de lista'
      
      return 'Elemento'
    },

    activateElement() {
      if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
        const element = this.readableElements[this.currentElementIndex]
        
        if (this.isAccordionButton(element)) {
          this.handleAccordionInteraction(element)
          return
        }
        
        if (this.isInteractiveElement(element)) {
          this.announceChange('Ativando elemento...')
          
          if (element.click) {
            element.click()
          } else {
            const event = new MouseEvent('click', {
              bubbles: true,
              cancelable: true
            })
            element.dispatchEvent(event)
          }
          
          setTimeout(() => {
            this.gatherReadableElements()
            this.announceChange('Elemento ativado')
          }, 500)
        } else {
          this.announceChange('Elemento não é interativo')
        }
      }
    },

    // handleAccordionInteraction(element) {
    //   const isExpanded = element.getAttribute('aria-expanded') === 'true'
      
    //   this.announceChange(isExpanded ? 'Recolhendo accordion...' : 'Expandindo accordion...')
      
    //   element.click()
      
    //   setTimeout(() => {
    //     this.gatherReadableElements()
        
    //     if (!isExpanded) {
    //       const targetId = element.getAttribute('data-bs-target') || 
    //                       element.getAttribute('aria-controls')
    //       if (targetId) {
    //         const targetElement = document.querySelector(targetId)
    //         if (targetElement) {
    //           const firstChildElement = this.findFirstReadableChild(targetElement)
    //           if (firstChildElement) {
    //             const newIndex = this.readableElements.indexOf(firstChildElement)
    //             if (newIndex !== -1) {
    //               this.currentElementIndex = newIndex
    //               this.highlightCurrentElement()
    //             }
    //           }
    //         }
    //       }
    //     }
        
    //     this.announceChange(`Accordion ${isExpanded ? 'recolhido' : 'expandido'}`)
    //   }, 500)
    // },

    findFirstReadableChild(container) {
      const selector = `
        h1, h2, h3, h4, h5, h6,
        p,
        a:not([aria-hidden="true"]),
        button,
        input,
        textarea,
        select,
        label,
        li,
        td,
        th,
        img,
        svg[aria-label]
      `
      
      const elements = container.querySelectorAll(selector)
      for (let el of elements) {
        if (this.isElementVisible(el) && !el.closest('[data-screen-reader-ignore]')) {
          return el
        }
      }
      return null
    },

    exitAccordion() {
      const currentElement = this.readableElements[this.currentElementIndex]
      if (!currentElement) return
      
      const accordionItem = currentElement.closest('.accordion-item')
      if (!accordionItem) return
      
      const accordionButton = accordionItem.querySelector('.accordion-button')
      if (!accordionButton) return
      
      const buttonIndex = this.readableElements.indexOf(accordionButton)
      if (buttonIndex === -1) return
      
      this.currentElementIndex = buttonIndex
      this.highlightCurrentElement()
      this.announceChange('Saiu do conteúdo do accordion')
    },

    isInteractiveElement(element) {
      const tag = element.tagName.toLowerCase()
      const interactiveTags = ['button', 'a', 'input', 'textarea', 'select']
      
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

    increaseRate() {
      if (!this.speechSynth) return

      const currentRate = this.utterance ? this.utterance.rate : this.speechRate
      const newRate = Math.min(currentRate + 0.1, 2.0)

      if (this.utterance) {
        this.utterance.rate = newRate
      }

      this.speechRate = newRate
      this.announceChange(`Velocidade: ${Math.round(newRate * 10) / 10}x`)
    },

    decreaseRate() {
      if (!this.speechSynth) return

      const currentRate = this.utterance ? this.utterance.rate : this.speechRate
      const newRate = Math.max(currentRate - 0.1, 0.5)

      if (this.utterance) {
        this.utterance.rate = newRate
      }

      this.speechRate = newRate
      this.announceChange(`Velocidade: ${Math.round(newRate * 10) / 10}x`)
    },

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
        case "Enter":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.activateElement()
            event.preventDefault()
          }
          break
        case "Backspace":
          if (!event.ctrlKey && !event.altKey && !event.metaKey) {
            this.exitAccordion()
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