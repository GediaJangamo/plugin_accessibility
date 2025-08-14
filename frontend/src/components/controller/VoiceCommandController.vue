<template>
  <div v-if="showComponent">
    <!-- Controlador de Voz - Versão melhorada -->
    <div class="fixed inset-x-0 bottom-6 mx-auto z-50 flex items-center justify-between bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 w-full max-w-2xl px-2 py-6">
      <!-- Área principal -->
      <div class="flex items-center flex-1 gap-3">
        <!-- Botão de microfone -->
        <button 
          ref="micButton"
          @click="toggleRecognition"
          class="relative w-10 h-10 rounded-full flex items-center justify-center transition-all focus:outline-none"
          :class="isListening ? 'bg-green-500 hover:bg-green-600 shadow-lg' : 'bg-red-500 hover:bg-red-600'"
          :aria-label="isListening ? 'Desativar microfone' : 'Ativar microfone'"
        >
          <div v-if="!isListening" class="absolute w-8 h-1 bg-white rotate-45 rounded-full z-10"></div>
          <div v-if="recognitionState === 'listening'" class="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-green-300 animate-ping"></div>
          
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white relative z-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </button>

        <!-- Status -->
        <div class="flex-1 min-w-0 py-2 px-3 rounded-full text-white" :class="getStatusColor()">
          <div class="flex items-center justify-between  gap-2">
            <p class="text-sm font-medium truncate">{{ statusMessage }}</p>
          </div>
          
          <p v-if="lastTranscript && isListening" class="text-xs mt-1 truncate opacity-90 bg-black/10 px-2 py-1 rounded-full">
            "{{ lastTranscript }}"
          </p>
          
          <!-- <p v-if="recognitionState === 'thinking'" class="text-xs mt-1 animate-pulse opacity-90">
            Processando...
          </p> -->
          
          <p v-if="recognitionState === 'navigating'" class="text-xs mt-1 animate-pulse">
            Carregando...
          </p>
        </div>
      </div>

      <!-- Controles - Agrupados e mais compactos -->
      <div class="flex items-center gap-1 ml-1">
        <!-- Botão de comandos -->
        <button 
          @click="toggleCommandsList"
          class=" p-2 rounded-full text-white hover:bg-[#3b82f6] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#3b82f6] transition-colors bg-[#3b82f6]"
          :aria-label="showCommandsList ? 'Ocultar lista de comandos' : 'Mostrar lista de comandos'"
          :title="showCommandsList ? 'Ocultar comandos' : 'Ver todos os comandos'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </button>

        <!-- Botão de áudio -->
        <button 
          @click="toggleSpeaker"
          class="p-2 rounded-full text-white transition-colors"
          :class="speakerEnabled ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-500 hover:bg-gray-600'"
          :aria-label="speakerEnabled ? 'Desativar áudio' : 'Ativar áudio'"
        >
          <svg v-if="speakerEnabled" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="m19.07 4.93-1.41 1.41A9 9 0 0 1 20 12a9 9 0 0 1-2.34 5.66l1.41 1.41A11 11 0 0 0 22 12a11 11 0 0 0-2.93-7.07zM15.54 8.46a5 5 0 0 1 0 7.07l1.41 1.41a7 7 0 0 0 0-9.9z"></path>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <line x1="23" y1="9" x2="17" y2="15"></line>
            <line x1="17" y1="9" x2="23" y2="15"></line>
          </svg>
        </button>

        <!-- Botão de fechar -->
        <button 
          @click="closeController"
          class="p-2 rounded-full text-white bg-red-500 hover:bg-red-600 transition-colors"
          aria-label="Fechar controlador"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Modal de Comandos - Versão melhorada -->
   <div 
  v-if="showCommandsList" 
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
>
  <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] overflow-hidden flex flex-col">
    <!-- Header -->
    <div class="p-6 bg-gradient-to-r from-[#3b82f6] to-[#1d4ed8] dark:from-[#1d4ed8] dark:to-[#1e3a8a]">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="bg-white bg-opacity-20 p-2 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-white">
            Comandos de Voz Disponíveis
          </h2>
        </div>
        <button 
          @click="closeCommandsList" 
          class="text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white rounded-full p-1 transition-colors"
          aria-label="Fechar menu de ajuda"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <p class="text-blue-100 mt-2 max-w-2xl">
        Utilize estes comandos para navegar pelo sistema usando apenas sua voz. Diga "ajuda" a qualquer momento para ver esta lista.
      </p>
    </div>
    
    <!-- Content -->
    <div class="p-6 overflow-auto">
      <!-- Navegação Geral -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-[#3b82f6] dark:text-[#93c5fd] mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
          Navegação Geral
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="(command, commandKey) in commandCategories.navegacao.commands" :key="commandKey" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-200 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              {{ commandKey }}
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              {{ command.description }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Comandos do Sistema -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-[#3b82f6] dark:text-[#93c5fd] mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
          Módulos do Sistema
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="(command, commandKey) in commandCategories.modulos.commands" :key="commandKey" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              {{ commandKey }}
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              {{ command.description }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Comandos de Acessibilidade -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-[#3b82f6] dark:text-[#93c5fd] mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
          Acessibilidade
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="(command, commandKey) in commandCategories.acessibilidade.commands" :key="commandKey" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              {{ commandKey }}
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              {{ command.description }}
            </div>
          </div>
        </div>
      </div>

      <!-- Atalhos Importantes -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-[#3b82f6] dark:text-[#93c5fd] mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
          Atalhos Importantes
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              ler página
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              Lê todo o conteúdo da página atual
            </div>
          </div>
          <div class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              parar leitura
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              Para a leitura em andamento
            </div>
          </div>
          <div class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              tecla M
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              Ativa ou desativa o microfone
            </div>
          </div>
          <div class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
            <div class="font-mono text-sm bg-blue-50 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
              ajuda [categoria]
            </div>
            <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
              Mostra comandos de uma categoria específica
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-blue-50 dark:bg-gray-800">
      <div class="flex items-center justify-between">
        <p class="text-sm text-[#3b82f6] dark:text-[#93c5fd]">
          <span class="font-bold">Dica:</span> Você pode dizer "ajuda" a qualquer momento para ver estes comandos novamente.
        </p>
        <button 
          @click="closeCommandsList"
          class="px-4 py-2 bg-[#3b82f6] hover:bg-[#1d4ed8] text-white rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-[#3b82f6] focus:ring-offset-2"
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script>
export default {
  name: 'VoiceCommandController',
  props: {
    active: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      recognition: null,
      synthesis: null,
      isListening: false,
      speakerEnabled: true,
      showComponent: false,
      showCommandsList: false,
      errorCount: 0,
      lastCommand: '',
      lastTranscript: '',
      recognitionMessage: '',
      recognitionState: 'silenced',
      navigationHistory: [],
      currentPage: '',
      helpMode: false,
      currentHelpCategory: null,
      isNavigating: false,
      isReading: false,
      keyboardListener: null,
      
      // Comandos organizados por categoria
      commandCategories: {
        navegacao: {
          name: 'Navegação Geral',
          commands: {
            "ir para início": { action: "/dashboard/", description: "Navega para a página inicial" },
            "voltar": { action: "history_back", description: "Retorna à página anterior" },
            "avançar": { action: "history_forward", description: "Avança para a próxima página" },
            "rolar para baixo": { action: "scroll_down", description: "Rola a página para baixo" },
            "rolar para cima": { action: "scroll_up", description: "Rola a página para cima" },
            "atualizar página": { action: "reload_page", description: "Recarrega a página atual" },
            "onde estou": { action: "announce_location", description: "Informa a página atual" },
            "repetir última ação": { action: "repeat_last", description: "Repete o último comando executado" },
            "ler página": { action: "read_page_content", description: "Lê todo o conteúdo da página atual" },
            "parar leitura": { action: "stop_reading", description: "Para a leitura em andamento" }
          }
        },
        modulos: {
          name: 'Módulos do Sistema',
          commands: {
            "abrir avaliações": { action: "/painel_estudante/avaliacoes/", description: "Acede ao módulo de avaliações" },
            "abrir inscrições": { action: "/painel_estudante/inscricoes/", description: "Acede ao módulo de inscrições" },
            "abrir matrículas": { action: "/painel_estudante/matriculas/", description: "Acede ao módulo de matrículas" },
            "abrir faturas": { action: "/painel_estudante/facturas/", description: "Acede ao módulo de faturas" },
            "abrir mensalidades": { action: "/painel_estudante/mensalidades/", description: "Acede ao módulo de mensalidades" },
            "abrir vula": { action: "/painel_estudante/vula/", description: "Acede à plataforma Vula" },
            "abrir perfil": { action: "/painel_estudante/", description: "Acede ao perfil do utilizador" },
            "ir para painel": { action: "/painel_estudante/", description: "Volta ao painel principal" }
          }
        },
        acessibilidade: {
          name: 'Acessibilidade',
          commands: {
            "ativar alto contraste": { action: "toggle_high_contrast", description: "Ativa o modo de alto contraste" },
            "desativar alto contraste": { action: "toggle_high_contrast", description: "Desativa o modo de alto contraste" },
            "aumentar fonte": { action: "increase_font_size", description: "Aumenta o tamanho da fonte" },
            "diminuir fonte": { action: "decrease_font_size", description: "Diminui o tamanho da fonte" },
            "tamanho normal": { action: "reset_font_size", description: "Restaura fonte ao tamanho padrão" },
            "ativar áudio": { action: "enable_audio", description: "Ativa feedback de voz" },
            "desativar áudio": { action: "disable_audio", description: "Desativa feedback de voz" }
          }
        }
      },
      
      // Comandos especiais do sistema
      systemCommands: {
        "ajuda": "show_help_categories"
      }
    }
  },
  computed: {
    statusMessage() {
      if (this.helpMode) {
        return this.currentHelpCategory ? 
          `Ajuda: ${this.commandCategories[this.currentHelpCategory].name}` : 
          'Modo ajuda ativo';
      }
      
      switch(this.recognitionState) {
        case 'listening':
          return 'Ouvindo comandos...';
        case 'thinking':
          return 'Processando comando...';
        case 'navigating':
          return 'Carregando página...';
        case 'error':
          return `Erro: ${this.recognitionMessage}`;
        case 'silenced':
          if (this.isListening) {
            return 'Microfone ativo - Diga um comando ou pressione M';
          } else {
            return 'Sistema ativo - Pressione M para ativar microfone ou clique no botão';
          }
        default:
          return 'Sistema pronto';
      }
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.showComponent = true;
          this.initializeSystem();
        } else {
          this.showComponent = false;
          this.stopVoiceRecognition();
          this.removeKeyboardListener();
        }
      }
    }
  },
  mounted() {
    this.initializeSpeechSynthesis();
    this.detectCurrentPage();
    this.addKeyboardListener();
    
    // Foca no botão de microfone quando o componente é montado
    this.$nextTick(() => {
      if (this.$refs.micButton) {
        this.$refs.micButton.focus();
      }
    });
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    // Lista de comandos
    toggleCommandsList() {
      this.showCommandsList = !this.showCommandsList;
      if (this.showCommandsList) {
        this.speak('Lista de comandos aberta');
      }
    },

    closeCommandsList() {
      this.showCommandsList = false;
      this.speak('Lista de comandos fechada');
    },

    // Listener de teclado
    addKeyboardListener() {
      this.keyboardListener = (event) => {
        // Fecha lista de comandos com ESC
        if (event.key === 'Escape' && this.showCommandsList) {
          this.closeCommandsList();
          return;
        }
        
        // Verifica se não está digitando em um campo de texto
        if (event.target.tagName.toLowerCase() === 'input' || 
            event.target.tagName.toLowerCase() === 'textarea' ||
            event.target.contentEditable === 'true') {
          return;
        }
        
        if (event.key.toLowerCase() === 'm' && !event.ctrlKey && !event.altKey && !event.metaKey) {
          event.preventDefault();
          this.toggleRecognition();
        }
      };
      
      document.addEventListener('keydown', this.keyboardListener);
    },

    removeKeyboardListener() {
      if (this.keyboardListener) {
        document.removeEventListener('keydown', this.keyboardListener);
        this.keyboardListener = null;
      }
    },

    // Inicialização do sistema
    initializeSystem() {
      this.speak('Sistema de comandos de voz ativado. Pressione M para ativar o microfone ou diga "ajuda" seguido de uma categoria para conhecer os comandos.');
      this.detectCurrentPage();
    },

    // Text-to-Speech com velocidade ajustada
    initializeSpeechSynthesis() {
      if ('speechSynthesis' in window) {
        this.synthesis = window.speechSynthesis;
      }
    },

    speak(text, priority = 'normal') {
      if (!this.speakerEnabled || !this.synthesis) return;
      
      // Cancela falas anteriores se for alta prioridade
      if (priority === 'high') {
        this.synthesis.cancel();
        this.isReading = false;
      }
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-BR';
      utterance.rate = 0.7; // Velocidade mais lenta
      utterance.pitch = 1.0;
      utterance.volume = 0.8;
      
      // Seleciona voz em português se disponível
      const voices = this.synthesis.getVoices();
      const portugueseVoice = voices.find(voice => 
        voice.lang.includes('pt') || voice.lang.includes('PT')
      );
      if (portugueseVoice) {
        utterance.voice = portugueseVoice;
      }

      // Marca como lendo se for leitura de página
      if (text.length > 200) {
        this.isReading = true;
        utterance.onend = () => {
          this.isReading = false;
        };
      }
      
      this.synthesis.speak(utterance);
    },

    // Controles de áudio
    toggleSpeaker() {
      this.speakerEnabled = !this.speakerEnabled;
      const message = this.speakerEnabled ? 
        'Feedback de voz ativado' : 
        'Feedback de voz desativado';
      
      if (this.speakerEnabled) {
        this.speak(message);
      }
      
      this.$emit('announce', message);
    },

    // Fechar controlador
     closeController() {
      this.showComponent = false;
      this.speak('Controlador de voz fechado');
      this.$emit('close'); 
      this.$emit('update:active', false);
    },

    // Detecção de página atual
    detectCurrentPage() {
      const path = window.location.pathname;
      const pageNames = {
        '/dashboard/': 'Painel Principal',
        '/painel_estudante/': 'Painel do Estudante',
        '/painel_estudante/avaliacoes/': 'Avaliações',
        '/painel_estudante/inscricoes/': 'Inscrições',
        '/painel_estudante/matriculas/': 'Matrículas',
        '/painel_estudante/facturas/': 'Faturas',
        '/painel_estudante/mensalidades/': 'Mensalidades',
        '/painel_estudante/vula/': 'Plataforma Vula'
      };
      
      this.currentPage = pageNames[path] || 'Página não identificada';
    },

    // Leitura do conteúdo da página
    readPageContent() {
      if (this.isReading) {
        this.speak('Já está a ler conteúdo. Diga "parar leitura" para interromper.');
        return;
      }

      this.speak('A iniciar leitura da página', 'high');
      this.isReading = true;
      
      // Para a leitura atual se houver
      this.synthesis.cancel();
      
      setTimeout(() => {
        // Coleta texto principal da página
        const content = this.extractPageContent();
        if (content.trim()) {
          this.speak(content);
        } else {
          this.speak('Não foi possível encontrar conteúdo de texto nesta página');
          this.isReading = false;
        }
      }, 1000);
    },

    extractPageContent() {
      // Remove elementos que não devem ser lidos
      const excludeSelectors = [
        'script', 'style', 'nav', 'header', 'footer', 
        '.voice-controller', '[aria-hidden="true"]',
        '.breadcrumb', '.pagination'
      ];
      
      // Prioriza elementos principais
      const prioritySelectors = [
        'main', '.main-content', '#content', '.content',
        'article', '.article', 'section', '.section'
      ];
      
      let content = '';
      
      // Tenta encontrar conteúdo principal primeiro
      for (const selector of prioritySelectors) {
        const element = document.querySelector(selector);
        if (element) {
          content = this.getTextContent(element, excludeSelectors);
          break;
        }
      }
      
      // Se não encontrou conteúdo principal, usa o body
      if (!content.trim()) {
        content = this.getTextContent(document.body, excludeSelectors);
      }
      
      // Limita o tamanho do texto
      const words = content.split(/\s+/);
      if (words.length > 150) {
        content = words.slice(0, 150).join(' ') + '... Conteúdo truncado.';
      }
      
      return content;
    },

    getTextContent(element, excludeSelectors) {
      const clone = element.cloneNode(true);
      
      // Remove elementos excluídos
      excludeSelectors.forEach(selector => {
        const elements = clone.querySelectorAll(selector);
        elements.forEach(el => el.remove());
      });
      
      // Extrai o texto
      let text = clone.textContent || clone.innerText || '';
      
      // Limpa o texto
      text = text.replace(/\s+/g, ' ').trim();
      text = text.replace(/\n{3,}/g, '\n\n');
      
      return text;
    },

    stopReading() {
      this.synthesis.cancel();
      this.isReading = false;
      this.speak('Leitura interrompida');
    },

    // Obter cor do status
    getStatusColor() {
      if (this.helpMode) {
        return 'bg-green-500 dark:bg-green-600';
      }
      
      switch(this.recognitionState) {
        case 'listening':
          return 'bg-green-500 dark:bg-green-600';
        case 'thinking':
          return 'bg-blue-500 dark:bg-blue-600';
        case 'navigating':
          return 'bg-orange-500 dark:bg-orange-600';
        case 'error':
          return 'bg-red-500 dark:bg-red-600';
        default:
          return 'bg-gray-500 dark:bg-gray-600';
      }
    },

    // Controle de reconhecimento de voz
    toggleRecognition() {
      if (this.isListening) {
        this.stopVoiceRecognition();
      } else {
        this.startVoiceRecognition();
      }
    },

    startVoiceRecognition() {
      if (!this.active) {
        this.speak('Os comandos de voz estão desativados');
        return;
      }
      
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        try {
          if (this.recognition) {
            this.recognition.stop();
          }
          
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = true;
          this.recognition.interimResults = false;
          this.recognition.lang = 'pt-BR';
          this.recognition.maxAlternatives = 5;
          
          this.recognition.onstart = () => {
            this.isListening = true;
            this.recognitionState = 'listening';
          };
          
          this.recognition.onend = () => {
            // Reinicia automaticamente se ainda estiver ativo e não estiver navegando
            if (this.isListening && this.recognitionState === 'listening' && !this.isReading) {
              setTimeout(() => {
                if (this.isListening && this.recognitionState === 'listening' && !this.isReading) {
                  try {
                    this.recognition.start();
                  } catch (e) {
                    console.error('Erro ao reiniciar:', e);
                  }
                }
              }, 1000);
            }
          };
          
          this.recognition.onerror = (event) => {
            console.error('Erro de reconhecimento:', event.error);
            
            if (event.error === 'not-allowed') {
              this.speak('Permissão de microfone negada. Por favor, permita o acesso ao microfone.');
            } else if (event.error === 'network') {
              this.speak('Erro de conexão. Verifique sua internet.');
            } else if (event.error !== 'no-speech' && event.error !== 'aborted') {
              this.speak('Erro no reconhecimento de voz. Pressione M para tentar novamente.');
            }
          };
          
          this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            this.lastTranscript = transcript;
            this.recognitionState = 'thinking';
            
            if (transcript !== this.lastCommand) {
              this.lastCommand = transcript;
              this.processVoiceCommand(transcript);
            }
            
            setTimeout(() => {
              if (this.recognitionState === 'thinking') {
                this.recognitionState = 'listening';
              }
            }, 2000);
          };
          
          setTimeout(() => {
            try {
              this.recognition.start();
              this.speak('Microfone ativado');
            } catch (e) {
              this.speak('Erro ao iniciar o microfone');
            }
          }, 300);
          
        } catch (error) {
          this.speak('Erro ao inicializar o reconhecimento de voz');
        }
      } else {
        this.speak('Seu navegador não suporta reconhecimento de voz');
      }
    },

    stopVoiceRecognition() {
      if (this.recognition) {
        try {
          this.recognition.stop();
        } catch (e) {
          console.error('Erro ao parar:', e);
        }
        this.recognition = null;
      }
      
      this.isListening = false;
      this.recognitionState = 'silenced';
      this.speak('Microfone desativado. Pressione M para reativar.');
    },

    // Sistema de ajuda simplificado
    showHelpForCategory(categoryKey) {
      const category = this.commandCategories[categoryKey];
      if (!category) {
        this.speak('Categoria não encontrada');
        return;
      }
      
      this.helpMode = true;
      this.currentHelpCategory = categoryKey;
      
      const commands = Object.keys(category.commands);
      
      this.speak(`Comandos da categoria ${category.name}:`);
      
      // Lê cada comando com uma pausa menor
      commands.forEach((command, index) => {
        setTimeout(() => {
          const description = category.commands[command].description;
          this.speak(`${command}: ${description}`, 'normal');
        }, (index + 1) * 2500); // Reduzido de 3000 para 2500
      });
      
      // Sai do modo ajuda automaticamente após terminar
      setTimeout(() => {
        this.helpMode = false;
        this.currentHelpCategory = null;
        this.speak('Pode agora usar qualquer comando normalmente.');
      }, (commands.length + 1) * 2500);
    },

    // Processamento de comandos melhorado
    processVoiceCommand(command) {
      console.log('Comando recebido:', command);
      
      // Se estiver lendo, prioriza comandos de parar
      if (this.isReading) {
        if (command.includes('parar') || command.includes('pausa') || command.includes('stop')) {
          this.stopReading();
          return;
        }
        // Ignora outros comandos durante a leitura
        this.speak('Diga "parar leitura" para interromper e usar outros comandos');
        return;
      }
      
      // Comando de ajuda com categoria
      if (command.includes('ajuda')) {
        const words = command.split(/\s+/);
        const helpIndex = words.findIndex(word => word.includes('ajuda'));
        
        if (helpIndex !== -1 && helpIndex < words.length - 1) {
          // Há uma categoria após "ajuda"
          const categoryName = words.slice(helpIndex + 1).join(' ');
          const categoryKey = this.findCategoryByName(categoryName);
          
          if (categoryKey) {
            this.showHelpForCategory(categoryKey);
            return;
          }
        }
        
        // Ajuda geral - lista categorias
        const categories = Object.keys(this.commandCategories);
        const categoryNames = categories.map(key => this.commandCategories[key].name);
        this.speak(`Categorias disponíveis: ${categoryNames.join(', ')}. Diga "ajuda" seguido do nome da categoria para ouvir seus comandos.`);
        return;
      }
      
      // Comandos especiais
      if (command.includes('onde estou')) {
        this.detectCurrentPage();
        this.speak(`Você está na página: ${this.currentPage}`);
        return;
      }

      if (command.includes('ler página') || command.includes('ler conteúdo')) {
        this.readPageContent();
        return;
      }

      if (command.includes('parar leitura') || command.includes('parar')) {
        this.stopReading();
        return;
      }
      
      if (command.includes('repetir')) {
        if (this.navigationHistory.length > 0) {
          const lastAction = this.navigationHistory[this.navigationHistory.length - 1];
          this.speak(`Repetindo: ${lastAction}`);
          this.executeVoiceCommand(lastAction);
        } else {
          this.speak('Nenhuma ação anterior para repetir');
        }
        return;
      }
      
      // Sai do modo ajuda se executar comando normal
      if (this.helpMode) {
        this.helpMode = false;
        this.currentHelpCategory = null;
      }
      
      // Procura comando em todas as categorias
      const foundCommand = this.findCommand(command);
      
      if (foundCommand) {
        this.executeVoiceCommand(foundCommand.command, foundCommand.action);
      } else {
        this.speak('Comando não reconhecido. Clique no ícone de lista para ver todos os comandos ou diga "ajuda" seguido de uma categoria.');
      }
    },

    // Busca categoria por nome melhorada
    findCategoryByName(name) {
      name = name.toLowerCase();
      
      // Mapeamento direto de palavras-chave
      const keywordMap = {
        'navegação': 'navegacao',
        'navegacao': 'navegacao',
        'navegar': 'navegacao',
        'página': 'navegacao',
        'pagina': 'navegacao',
        'módulos': 'modulos',
        'modulos': 'modulos',
        'sistema': 'modulos',
        'aplicação': 'modulos',
        'aplicacao': 'modulos',
        'acessibilidade': 'acessibilidade',
        'acesso': 'acessibilidade',
        'visual': 'acessibilidade',
        'contraste': 'acessibilidade',
        'fonte': 'acessibilidade'
      };
      
      // Procura por palavras-chave
      for (const [keyword, categoryKey] of Object.entries(keywordMap)) {
        if (name.includes(keyword)) {
          return categoryKey;
        }
      }
      
      // Busca por similaridade com nomes das categorias
      for (const [key, category] of Object.entries(this.commandCategories)) {
        const categoryName = category.name.toLowerCase();
        if (categoryName.includes(name) || name.includes(categoryName)) {
          return key;
        }
      }
      
      return null;
    },

    // Busca comando em todas as categorias
    findCommand(inputCommand) {
      let bestMatch = null;
      let bestScore = 0;
      
      // Busca em todas as categorias
      for (const category of Object.values(this.commandCategories)) {
        for (const [command, data] of Object.entries(category.commands)) {
          const score = this.getSimilarityScore(inputCommand, command);
          if (score > bestScore && score > 0.6) {
            bestScore = score;
            bestMatch = { command, action: data.action };
          }
        }
      }
      
      return bestMatch;
    },

    // Cálculo de similaridade
    getSimilarityScore(str1, str2) {
      str1 = str1.toLowerCase().trim();
      str2 = str2.toLowerCase().trim();
      
      if (str1.includes(str2) || str2.includes(str1)) {
        return 0.9;
      }
      
      const words1 = str1.split(/\s+/);
      const words2 = str2.split(/\s+/);
      
      let commonWords = 0;
      let significantWords = 0;
      
      words1.forEach(word => {
        if (word.length > 2) {
          significantWords++;
          if (words2.some(w => w.includes(word) || word.includes(w))) {
            commonWords++;
          }
        }
      });
      
      return significantWords > 0 ? commonWords / significantWords : 0;
    },

    // Execução de comandos
    executeVoiceCommand(command, action) {
      console.log('Executando comando:', command);
      
      // Adiciona à história de navegação
      this.navigationHistory.push(command);
      if (this.navigationHistory.length > 10) {
        this.navigationHistory.shift();
      }
      
      // Ações especiais (não navegação)
      if (typeof action === 'string' && !action.startsWith('/')) {
        this.executeSpecialAction(action, command);
        return;
      }
      
      // Navega para URLs
      if (action.startsWith('/')) {
        this.navigateToUrl(action, command);
      }
    },

    // Ações especiais (não navegação)
    executeSpecialAction(action) {
      switch(action) {
        case 'history_back':
          window.history.back();
          this.speak('Voltando para página anterior');
          setTimeout(() => {
            this.detectCurrentPage();
          }, 1500);
          break;
          
        case 'history_forward':
          window.history.forward();
          this.speak('Avançando para próxima página');
          setTimeout(() => {
            this.detectCurrentPage();
          }, 1500);
          break;
          
        case 'scroll_down':
          window.scrollBy({ top: 400, behavior: 'smooth' });
          this.speak('Rolando para baixo');
          break;
          
        case 'scroll_up':
          window.scrollBy({ top: -400, behavior: 'smooth' });
          this.speak('Rolando para cima');
          break;
          
        case 'reload_page':
          this.speak('Recarregando página');
          setTimeout(() => window.location.reload(), 1000);
          break;
          
        case 'announce_location':
          this.detectCurrentPage();
          this.speak(`Você está em: ${this.currentPage}`);
          break;

        case 'read_page_content':
          this.readPageContent();
          break;

        case 'stop_reading':
          this.stopReading();
          break;
          
        case 'toggle_high_contrast': {
          document.body.classList.toggle('high-contrast');
          const isActive = document.body.classList.contains('high-contrast');
          this.speak(isActive ? 'Alto contraste ativado' : 'Alto contraste desativado');
          break;
        }
        
        case 'increase_font_size':
          this.adjustFontSize(1.1);
          this.speak('Fonte aumentada');
          break;
          
        case 'decrease_font_size':
          this.adjustFontSize(0.9);
          this.speak('Fonte diminuída');
          break;
          
        case 'reset_font_size':
          document.documentElement.style.fontSize = '16px';
          this.speak('Fonte restaurada');
          break;
          
        case 'enable_audio':
          this.speakerEnabled = true;
          this.speak('Áudio ativado');
          break;
          
        case 'disable_audio':
          this.speakerEnabled = false;
          // Não fala após desativar
          break;
          
        default:
          this.speak('Ação não reconhecida');
      }
    },

    // Ajuste do tamanho da fonte
    adjustFontSize(factor) {
      const currentSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
      const newSize = Math.max(12, Math.min(24, currentSize * factor));
      document.documentElement.style.fontSize = newSize + 'px';
    },

    // Navegação para URLs
    navigateToUrl(url) {
      const pageNames = {
        '/dashboard/': 'Painel Principal',
        '/painel_estudante/': 'Painel do Estudante',
        '/painel_estudante/avaliacoes/': 'Avaliações',
        '/painel_estudante/inscricoes/': 'Inscrições', 
        '/painel_estudante/matriculas/': 'Matrículas',
        '/painel_estudante/facturas/': 'Faturas',
        '/painel_estudante/mensalidades/': 'Mensalidades',
        '/painel_estudante/vula/': 'Plataforma Vula'
      };
      
      const pageName = pageNames[url] || 'página solicitada';
      
      // Define estado de navegação
      this.recognitionState = 'navigating';
      this.isNavigating = true;
      
      // Desativa temporariamente o microfone durante a navegação
      const wasListening = this.isListening;
      if (this.isListening) {
        this.isListening = false;
        if (this.recognition) {
          this.recognition.stop();
        }
      }
      
      this.speak(`Abrindo ${pageName}`);
      
      // Navega para a URL
      setTimeout(() => {
        window.location.href = url;
        
        // Aguarda o carregamento da página
        const checkPageLoad = () => {
          if (document.readyState === 'complete') {
            setTimeout(() => {
              this.detectCurrentPage();
              this.recognitionState = 'silenced';
              this.isNavigating = false;
              
              // Confirma que chegou na página e reativa o microfone se estava ativo
              this.speak(`Você está agora no módulo de ${pageName}. Pressione M para ativar comandos de voz.`, 'high');
              
              if (wasListening) {
                setTimeout(() => {
                  this.startVoiceRecognition();
                }, 2000);
              }
            }, 1000);
          } else {
            setTimeout(checkPageLoad, 100);
          }
        };
        
        // Inicia a verificação do carregamento
        setTimeout(checkPageLoad, 500);
        
      }, 1000);
    },

    // Limpeza de recursos
    cleanup() {
      if (this.recognition) {
        this.recognition.stop();
        this.recognition = null;
      }
      
      if (this.synthesis) {
        this.synthesis.cancel();
      }
      
      this.removeKeyboardListener();
      this.isListening = false;
      this.isReading = false;
    }
  }
}
</script>

<style scoped>
/* Estilos para alto contraste */
:global(body.high-contrast) {
  filter: contrast(200%) brightness(150%);
}

/* Animações suaves */
.transition-colors {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Indicadores visuais melhorados */
.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

/* Estilos de foco melhorados */
button:focus {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}

/* Estilos para o popup de comandos */
.z-60 {
  z-index: 60;
}

/* Responsividade para dispositivos móveis */
@media (max-width: 640px) {
  .fixed {
    left: 1rem;
    right: 1rem;
    max-width: none;
  }
  
  .flex-grow {
    min-width: 0;
  }
  
  .text-sm {
    font-size: 0.875rem;
  }
  
  .text-xs {
    font-size: 0.75rem;
  }

  /* Ajustes para o popup em dispositivos móveis */
  .max-w-4xl {
    max-width: calc(100vw - 2rem);
  }
  
  .max-h-4xl {
    max-height: 80vh;
  }
}

/* Scrollbar customizada para o popup */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Efeitos hover melhorados */
.hover\:bg-purple-600:hover {
  background-color: rgb(194, 144, 240);
}

.hover\:bg-blue-600:hover {
  background-color: rgb(37 99 235);
}

.hover\:bg-gray-600:hover {
  background-color: rgb(75 85 99);
}

.hover\:bg-red-600:hover {
  background-color: rgb(220 38 38);
}
</style>