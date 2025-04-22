<template>
    <div 
      v-if="active"
      class="fixed bottom-5 left-1/2 transform -translate-x-1/2 bg-white dark:bg-gray-800 rounded-lg shadow-lg z-50 border border-gray-200 dark:border-gray-700"
      aria-live="polite"
    >
      <div class="flex items-center justify-between gap-2 p-3">
        <button 
          @click="playPause"
          class="flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          :aria-label="isPlaying ? 'Pausar leitura' : 'Iniciar leitura'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path v-if="!isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path v-if="isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
        
        <button 
          @click="previousElement"
          class="flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white p-3 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          aria-label="Elemento anterior"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <button 
          @click="nextElement"
          class="flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white p-3 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          aria-label="Próximo elemento"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
        
        <button 
          @click="restart"
          class="flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white p-3 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          aria-label="Reiniciar leitura"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
        
        <div class="px-3 text-gray-600 dark:text-gray-300 text-sm">
          {{ currentReadingStatus }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ScreenReaderControl',
    props: {
      active: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        isPlaying: false,
        readableElements: [],
        currentElementIndex: -1,
        speechSynth: null,
        utterance: null,
        currentReadingStatus: "Pronto para leitura"
      }
    },
    watch: {
      active: {
        immediate: true,
        handler(newValue) {
          if (newValue) {
            this.$nextTick(() => {
              this.initializeSpeechSynthesis();
              this.gatherReadableElements();
            });
          } else {
            this.stopSpeaking();
          }
        }
      }
    },
    methods: {
      initializeSpeechSynthesis() {
        if ('speechSynthesis' in window) {
        this.speechSynth = window.speechSynthesis;
        
        // Carrega as vozes disponíveis quando estiverem prontas
        if (this.speechSynth.onvoiceschanged !== undefined) {
          this.speechSynth.onvoiceschanged = this.loadVoices;
        }
        
        // Tenta carregar vozes imediatamente (para navegadores que já têm as vozes carregadas)
        this.loadVoices();
      } else {
        console.error('API de Síntese de Fala não suportada no navegador');
        this.currentReadingStatus = "Leitor não suportado";
      }
      },

      loadVoices() {
      // Este método ajuda a garantir que as vozes sejam carregadas corretamente
      if (this.speechSynth) {
        this.availableVoices = this.speechSynth.getVoices();
      }
      },
      
      gatherReadableElements() {
      // Seleciona apenas elementos dentro do conteúdo principal
      const mainContent = document.getElementById('main-content');
      if (!mainContent) {
        console.warn('Elemento #main-content não encontrado. Usando body como fallback.');
        // Se não encontrar o main-content, usa o body inteiro exceto o menu de acessibilidade
        const body = document.body;
        
        // Seleciona elementos de texto com conteúdo visível
        const selector = 'p, h1, h2, h3, h4, h5, h6, li, td, th, button:not([aria-hidden="true"]), a:not([aria-hidden="true"])';
        const allElements = body.querySelectorAll(selector);
        
        // Exclui elementos do menu de acessibilidade
        this.readableElements = Array.from(allElements).filter(el => {
          // Filtra elementos vazios ou ocultos ou dentro do menu de acessibilidade
          const text = el.textContent.trim();
          const isVisible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
          const isInAccessibilityMenu = el.closest('[role="dialog"]') !== null;
          return text && isVisible && !isInAccessibilityMenu;
        });
      } else {
        // Código original para quando o main-content existe
        const selector = 'p, h1, h2, h3, h4, h5, h6, li, td, th, button:not([aria-hidden="true"]), a:not([aria-hidden="true"])';
        const elements = mainContent.querySelectorAll(selector);
        
        this.readableElements = Array.from(elements).filter(el => {
          const text = el.textContent.trim();
          const isVisible = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
          return text && isVisible;
        });
      }
      if (this.readableElements.length > 0) {
        this.currentElementIndex = 0;
        this.highlightCurrentElement();
        this.currentReadingStatus = `${this.readableElements.length} elementos para ler`;
      } else {
        this.currentReadingStatus = "Nenhum conteúdo para ler";
      }
    },


      
      playPause() {
        if (this.isPlaying) {
          this.pauseSpeaking();
        } else {
          // Se não tiver elemento atual selecionado, comece pelo primeiro
          if (this.currentElementIndex === -1 && this.readableElements.length > 0) {
            this.currentElementIndex = 0;
          }
          this.speakCurrentElement();
        }
      },
      
      previousElement() {
        this.stopSpeaking();
        
        if (this.currentElementIndex > 0) {
          this.currentElementIndex--;
          this.highlightCurrentElement();
          this.updateReadingStatus();
          if (this.isPlaying) {
            this.speakCurrentElement();
          }
        }
      },
      
      nextElement() {
        this.stopSpeaking();
        
        if (this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++;
          this.highlightCurrentElement();
          this.updateReadingStatus();
          if (this.isPlaying) {
            this.speakCurrentElement();
          }
        }
      },
      
      restart() {
        this.stopSpeaking();
        this.currentElementIndex = 0;
        this.highlightCurrentElement();
        this.updateReadingStatus();
        if (this.isPlaying) {
          this.speakCurrentElement();
        }
      },
      
      speakCurrentElement() {
      if (!this.speechSynth || this.currentElementIndex < 0 || this.currentElementIndex >= this.readableElements.length) {
        return;
      }
      
      // Cancela qualquer fala anterior
      this.stopSpeaking();
      
      const currentElement = this.readableElements[this.currentElementIndex];
      const textToSpeak = currentElement.textContent.trim();
      
      this.utterance = new SpeechSynthesisUtterance(textToSpeak);
      
      // Tenta definir a voz em português do Brasil, se disponível
      const voices = this.speechSynth.getVoices();
      const portugueseVoice = voices.find(voice => 
        voice.lang.includes('pt-BR') || voice.lang.includes('pt')
      );
      
      if (portugueseVoice) {
        this.utterance.voice = portugueseVoice;
      }
      
      this.utterance.rate = 1.0;
      this.utterance.pitch = 1.0;
      this.utterance.lang = 'pt-BR';
      
      this.utterance.onend = () => {
        // Verifica se ainda está ativo e se há mais elementos
        if (this.active && this.currentElementIndex < this.readableElements.length - 1) {
          this.currentElementIndex++;
          this.highlightCurrentElement();
          this.updateReadingStatus();
          this.speakCurrentElement();
        } else {
          this.isPlaying = false;
          this.currentReadingStatus = "Leitura concluída";
        }
      };
      
      this.utterance.onerror = (event) => {
        console.error('Erro na síntese de fala:', event);
        this.isPlaying = false;
        this.currentReadingStatus = "Erro na leitura";
      };
      
      this.highlightCurrentElement();
      this.speechSynth.speak(this.utterance);
      this.isPlaying = true;
      this.updateReadingStatus();
    },
      
    pauseSpeaking() {
      if (this.speechSynth && this.isPlaying) {
        this.speechSynth.pause();
        this.isPlaying = false;
        this.currentReadingStatus = "Leitura pausada";
        
        // Alguns navegadores podem ter problemas com pause/resume
        // Então adiciona um temporizador para evitar que a síntese trave
        clearTimeout(this.pauseTimer);
        this.pauseTimer = setTimeout(() => {
          if (!this.isPlaying && this.speechSynth.paused) {
            // Força retomada se ficar pausado por muito tempo
            this.speechSynth.resume();
            this.speechSynth.pause();
          }
        }, 5000);
      }
    },

    resumeSpeaking() {
      if (this.speechSynth && this.speechSynth.paused) {
        clearTimeout(this.pauseTimer);
        this.speechSynth.resume();
        this.isPlaying = true;
        this.currentReadingStatus = `${this.currentElementIndex + 1} de ${this.readableElements.length}`;
      }
    },
      
      stopSpeaking() {
        if (this.speechSynth) {
          this.speechSynth.cancel();
          this.isPlaying = false;
        }
      },
      
      highlightCurrentElement() {
        // Remove destaque anterior
        document.querySelectorAll('.reading-highlight').forEach(el => {
          el.classList.remove('reading-highlight');
          el.style.outline = '';
        });
        
        // Adiciona novo destaque
        if (this.currentElementIndex >= 0 && this.readableElements[this.currentElementIndex]) {
          const element = this.readableElements[this.currentElementIndex];
          element.classList.add('reading-highlight');
          element.style.outline = '2px solid #077b4b';
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      },
      
      updateReadingStatus() {
        if (this.readableElements.length === 0) {
          this.currentReadingStatus = "Nenhum conteúdo para ler";
          return;
        }
        
        this.currentReadingStatus = `${this.currentElementIndex + 1} de ${this.readableElements.length}`;
      },

      // Adicione na seção methods
      debounceGatherElements() {
        if (this.gatherTimeout) clearTimeout(this.gatherTimeout);
        this.gatherTimeout = setTimeout(() => {
          this.gatherReadableElements();
        }, 300);
      },

      // Adicione a inicialização do MutationObserver no método mounted nao sei se deve estar aqui esse mounted e o bedore
      mounted() {
        // ... código existente ...
        
        // Observa mudanças no DOM para atualizar elementos legíveis
        if (window.MutationObserver) {
          this.observer = new MutationObserver(this.debounceGatherElements);
          this.observer.observe(document.body, { 
            childList: true, 
            subtree: true 
          });
        }
          // Adiciona atalhos de teclado quando o leitor estiver ativo
          window.addEventListener('keydown', this.handleKeyboardShortcuts);
      },
      
    },
    beforeUnmount() {
      this.stopSpeaking();
      // Remove destaques na página
      document.querySelectorAll('.reading-highlight').forEach(el => {
        el.classList.remove('reading-highlight');
        el.style.outline = '';
      });

      if (this.observer) {
          this.observer.disconnect();
        }
        window.removeEventListener('keydown', this.handleKeyboardShortcuts);
    },
    // Método para lidar com os atalhos de teclado
    handleKeyboardShortcuts(event) {
      // Só processa atalhos quando o componente está ativo
      if (!this.active) return;
      
      switch(event.key) {
        case 'p':
        case 'P':
        case ' ': // Espaço
          this.playPause();
          event.preventDefault();
          break;
        case 'ArrowRight':
          this.nextElement();
          event.preventDefault();
          break;
        case 'ArrowLeft':
          this.previousElement();
          event.preventDefault();
          break;
        case 'Home':
          this.restart();
          event.preventDefault();
          break;
        case 'Escape':
          this.$emit('update:active', false);
          event.preventDefault();
          break;
      }} 

  }
  </script>