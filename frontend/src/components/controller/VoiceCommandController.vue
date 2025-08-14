<template>
  <div v-if="showComponent">
    <div class="fixed inset-x-0 bottom-6 mx-auto z-50 flex items-center bg-white dark:bg-gray-800 rounded-lg p-4 shadow-lg border border-gray-200 dark:border-gray-700 w-full max-w-2xl justify-between">
      <div class="flex items-center space-x-4 flex-grow">
        <!-- Botão de microfone com atalhos universais -->
        <button 
          ref="micButton"
          @click="toggleRecognition"
          @keydown.enter="toggleRecognition"
          @keydown.space.prevent="toggleRecognition"
          class="relative w-12 h-12 rounded-full flex items-center justify-center transition-colors focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-600"
          :class="isListening ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'"
          :aria-label="isListening ? 'Desativar microfone' : 'Ativar microfone'"
          :title="isListening ? 'Microfone Ativo' : 'Microfone Inativo'"
        >
          <!-- Ícone de microfone cortado quando inativo -->
          <div v-if="!isListening" class="absolute w-10 h-1 bg-white rotate-45 rounded-full z-10"></div>
          
          <!-- Indicador de atividade quando ouvindo -->
          <div v-if="recognitionState === 'listening'" class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-green-300 animate-ping"></div>
          
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white relative z-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </button>

        <!-- Status do microfone com informações detalhadas -->
        <div class="flex-1 p-3 rounded-lg text-white" :class="getStatusColor()">
          <div class="flex items-center justify-between">
            <span class="font-medium text-sm">
              {{ statusMessage }}
            </span>
          </div>
          
          <!-- Último comando reconhecido -->
          <p v-if="lastTranscript && isListening" class="text-xs mt-1 opacity-90 bg-black bg-opacity-20 px-2 py-1 rounded">
            "{{ lastTranscript }}"
          </p>
          
          <!-- Indicador de processamento -->
          <p v-if="recognitionState === 'thinking'" class="text-xs mt-1 animate-pulse">
            Processando comando...
          </p>
        </div>
      </div>

      <!-- Botões de controle -->
      <div class="flex items-center space-x-2 ml-4">
        <!-- Botão de volume/speaker -->
        <button 
          @click="toggleSpeaker"
          @keydown.enter="toggleSpeaker"
          class="p-2 rounded-full text-white transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400"
          :class="speakerEnabled ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-500 hover:bg-gray-600'"
          :aria-label="speakerEnabled ? 'Desativar feedback de voz' : 'Ativar feedback de voz'"
          :title="speakerEnabled ? 'Áudio ativado' : 'Áudio desativado'"
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

        <!-- Botão de ajuda -->
        <button 
          @click="toggleHelpMenu"
          @keydown.enter="toggleHelpMenu"
          class="p-2 rounded-full text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400 transition-colors"
          aria-label="Abrir ajuda"
          title="Comandos disponíveis"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </button>

        <!-- Botão para fechar o controlador -->
        <button 
          @click="closeController"
          @keydown.enter="closeController"
          class="p-2 rounded-full text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 transition-colors"
          aria-label="Fechar controlador de voz"
          title="Fechar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Modal de ajuda aprimorado -->
    <div 
      v-if="showHelpMenu" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
      @keydown.escape="toggleHelpMenu"
    >
      <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Header -->
        <div class="p-6 bg-gradient-to-r from-blue-500 to-blue-700">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="bg-white bg-opacity-20 p-2 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                  <line x1="12" y1="19" x2="12" y2="23"></line>
                  <line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
              </div>
              <div>
                <h2 class="text-2xl font-bold text-white">Comandos de Voz e Atalhos</h2>
                <p class="text-blue-100 text-sm">Sistema de navegação acessível</p>
              </div>
            </div>
            <button 
              @click="toggleHelpMenu" 
              class="text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white rounded-full p-2 transition-colors"
              aria-label="Fechar menu de ajuda"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Content -->
        <div class="flex-1 overflow-auto p-6">
          <!-- Comandos de Voz -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Navegação Geral -->
            <div>
              <h3 class="text-lg font-bold text-green-600 dark:text-green-400 mb-3 border-b border-green-200 dark:border-green-700 pb-2">
                Navegação Geral
              </h3>
              <div class="space-y-2">
                <div v-for="(desc, cmd) in generalCommands" :key="cmd" class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
                  <div class="font-semibold text-green-800 dark:text-green-300 text-sm">"{{ cmd }}"</div>
                  <div class="text-green-700 dark:text-green-400 text-xs mt-1">{{ desc }}</div>
                </div>
              </div>
            </div>

            <!-- Comandos do Sistema -->
            <div>
              <h3 class="text-lg font-bold text-purple-600 dark:text-purple-400 mb-3 border-b border-purple-200 dark:border-purple-700 pb-2">
                Módulos do Sistema
              </h3>
              <div class="space-y-2">
                <div v-for="(desc, cmd) in systemCommands" :key="cmd" class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3">
                  <div class="font-semibold text-purple-800 dark:text-purple-300 text-sm">"{{ cmd }}"</div>
                  <div class="text-purple-700 dark:text-purple-400 text-xs mt-1">{{ desc }}</div>
                </div>
              </div>
            </div>

            <!-- Comandos de Acessibilidade -->
            <div>
              <h3 class="text-lg font-bold text-orange-600 dark:text-orange-400 mb-3 border-b border-orange-200 dark:border-orange-700 pb-2">
                Acessibilidade
              </h3>
              <div class="space-y-2">
                <div v-for="(desc, cmd) in accessibilityCommands" :key="cmd" class="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-3">
                  <div class="font-semibold text-orange-800 dark:text-orange-300 text-sm">"{{ cmd }}"</div>
                  <div class="text-orange-700 dark:text-orange-400 text-xs mt-1">{{ desc }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Leitura por voz -->
          <div class="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <h3 class="text-lg font-bold text-blue-600 dark:text-blue-400 mb-3">
              Leitura por Voz
            </h3>
            <p class="text-blue-700 dark:text-blue-300 text-sm mb-3">
              Para ouvir os comandos por categoria, diga um dos comandos abaixo:
            </p>
            <div class="space-y-2">
              <div class="bg-blue-100 dark:bg-blue-800/40 rounded p-2">
                <span class="font-semibold text-blue-800 dark:text-blue-300">"ler navegação"</span> - 
                <span class="text-blue-600 dark:text-blue-400">Lê comandos de navegação</span>
              </div>
              <div class="bg-blue-100 dark:bg-blue-800/40 rounded p-2">
                <span class="font-semibold text-blue-800 dark:text-blue-300">"ler módulos"</span> - 
                <span class="text-blue-600 dark:text-blue-400">Lê comandos dos módulos</span>
              </div>
              <div class="bg-blue-100 dark:bg-blue-800/40 rounded p-2">
                <span class="font-semibold text-blue-800 dark:text-blue-300">"ler acessibilidade"</span> - 
                <span class="text-blue-600 dark:text-blue-400">Lê comandos de acessibilidade</span>
              </div>
              <div class="bg-blue-100 dark:bg-blue-800/40 rounded p-2">
                <span class="font-semibold text-blue-800 dark:text-blue-300">"parar leitura"</span> - 
                <span class="text-blue-600 dark:text-blue-400">Interrompe a leitura atual</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <div class="flex items-center justify-between flex-wrap gap-4">
            <div class="text-sm text-gray-600 dark:text-gray-400">
              <p><strong>Dica:</strong> Active o microfone e diga os comandos naturalmente</p>
              <p><strong>Status:</strong> Microfone {{ isListening ? 'ATIVO' : 'INATIVO' }} | Áudio {{ speakerEnabled ? 'ATIVO' : 'INATIVO' }}</p>
            </div>
            <button 
              @click="toggleHelpMenu"
              class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400"
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
      showHelpMenu: false,
      showComponent: false,
      errorCount: 0,
      lastCommand: '',
      lastTranscript: '',
      recognitionMessage: '',
      recognitionState: 'silenced',
      navigationHistory: [],
      currentPage: '',
      isReading: false,
      
      // Comandos disponíveis
      generalCommands: {
        "ir para início": "Navega para a página inicial",
        "voltar": "Retorna à página anterior", 
        "avançar": "Avança para a próxima página",
        "rolar para baixo": "Rola a página para baixo",
        "rolar para cima": "Rola a página para cima",
        "atualizar página": "Recarrega a página atual",
        "onde estou": "Informa a página atual",
        "repetir última ação": "Repete o último comando executado"
      },
      systemCommands: {
        "abrir avaliações": "Acede ao módulo de avaliações",
        "abrir inscrições": "Acede ao módulo de inscrições", 
        "abrir matrículas": "Acede ao módulo de matrículas",
        "abrir faturas": "Acede ao módulo de faturas",
        "abrir mensalidades": "Acede ao módulo de mensalidades",
        "abrir vula": "Acede à plataforma Vula",
        "abrir perfil": "Acede ao perfil do utilizador",
        "ir para painel": "Volta ao painel principal"
      },
      accessibilityCommands: {
        "ativar alto contraste": "Ativa o modo de alto contraste",
        "desativar alto contraste": "Desativa o modo de alto contraste", 
        "aumentar fonte": "Aumenta o tamanho da fonte",
        "diminuir fonte": "Diminui o tamanho da fonte",
        "tamanho normal": "Restaura fonte ao tamanho padrão",
        "ativar áudio": "Ativa feedback de voz",
        "desativar áudio": "Desativa feedback de voz"
      }
    }
  },
  computed: {
    statusMessage() {
      switch(this.recognitionState) {
        case 'listening':
          return 'Ouvindo comandos...';
        case 'thinking':
          return 'Processando comando...';
        case 'error':
          return `Erro: ${this.recognitionMessage}`;
        case 'silenced':
          return this.isListening ? 'Microfone ativo - Diga um comando' : 'Microfone inativo - Clique para ativar';
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
        }
      }
    }
  },
  mounted() {
    this.initializeSpeechSynthesis();
    this.detectCurrentPage();
    
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
    // Inicialização do sistema
    initializeSystem() {
      this.speak('Sistema de comandos de voz ativado. Clique no botão do microfone para começar, ou no ícone de ajuda para ver todos os comandos.');
      this.detectCurrentPage();
    },

    // Text-to-Speech
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
      }
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-BR';
      utterance.rate = 0.9;
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

    // Controle do menu de ajuda
    toggleHelpMenu() {
      this.showHelpMenu = !this.showHelpMenu;
      const message = this.showHelpMenu ? 
        'Menu de ajuda aberto. Para ouvir comandos por categoria, diga: ler navegação, ler módulos, ou ler acessibilidade.' :
        'Menu de ajuda fechado.';
      this.speak(message);
    },

    // Fechar controlador
    closeController() {
      this.showComponent = false;
      this.speak('Controlador de voz fechado');
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

    // Obter cor do status
    getStatusColor() {
      switch(this.recognitionState) {
        case 'listening':
          return 'bg-green-500 dark:bg-green-600';
        case 'thinking':
          return 'bg-blue-500 dark:bg-blue-600';
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
            this.speak('Microfone ativado. Pode falar agora.');
          };
          
          this.recognition.onend = () => {
            // Reinicia automaticamente se ainda estiver ativo
            if (this.isListening && this.recognitionState !== 'silenced') {
              setTimeout(() => {
                if (this.isListening && this.showComponent) {
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
              this.speak('Erro no reconhecimento de voz. Tente novamente.');
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
      this.speak('Microfone desativado');
    },

    // Leitura por voz das categorias
    readCategory(category) {
      if (!this.speakerEnabled) {
        this.speak('Ative o áudio primeiro para ouvir os comandos');
        return;
      }
      
      this.isReading = true;
      this.synthesis.cancel(); // Para qualquer leitura anterior
      
      let commands;
      let categoryName;
      
      switch(category) {
        case 'navegacao':
          commands = this.generalCommands;
          categoryName = 'Navegação Geral';
          break;
        case 'modulos':
          commands = this.systemCommands;
          categoryName = 'Módulos do Sistema';
          break;
        case 'acessibilidade':
          commands = this.accessibilityCommands;
          categoryName = 'Acessibilidade';
          break;
        default:
          this.speak('Categoria não encontrada');
          return;
      }
      
      this.speak(`Comandos de ${categoryName}:`);
      
      const commandList = Object.entries(commands);
      let index = 0;
      
      const readNext = () => {
        if (index < commandList.length && this.isReading) {
          const [command, description] = commandList[index];
          this.speak(`${index + 1}: Diga "${command}" para ${description}`);
          index++;
          setTimeout(readNext, 4000);
        } else if (this.isReading) {
          this.speak('Fim da lista de comandos. Diga "parar leitura" para interromper ou escolha outra categoria.');
          this.isReading = false;
        }
      };
      
      setTimeout(readNext, 2000);
    },

    stopReading() {
      this.isReading = false;
      this.synthesis.cancel();
      this.speak('Leitura interrompida');
    },

    // Processamento de comandos
    processVoiceCommand(command) {
      console.log('Comando recebido:', command);
      
      // Comandos de leitura
      if (command.includes('ler navegação') || command.includes('ler navegacao')) {
        this.readCategory('navegacao');
        return;
      }
      
      if (command.includes('ler módulos') || command.includes('ler modulos')) {
        this.readCategory('modulos');
        return;
      }
      
      if (command.includes('ler acessibilidade')) {
        this.readCategory('acessibilidade');
        return;
      }
      
      if (command.includes('parar leitura')) {
        this.stopReading();
        return;
      }
      
      // Comandos especiais
      if (command.includes('onde estou')) {
        this.detectCurrentPage();
        this.speak(`Você está na página: ${this.currentPage}`);
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
      
      if (command.includes('ativar áudio')) {
        this.speakerEnabled = true;
        this.speak('Feedback de áudio ativado');
        return;
      }
      
      if (command.includes('desativar áudio')) {
        this.speakerEnabled = false;
        return;
      }
      
      // Procura correspondência nos comandos
      const allCommands = {
        ...this.generalCommands,
        ...this.systemCommands,
        ...this.accessibilityCommands
      };
      
      let bestMatch = null;
      let bestScore = 0;
      
      Object.keys(allCommands).forEach(cmd => {
        const score = this.getSimilarityScore(command, cmd);
        if (score > bestScore && score > 0.6) {
          bestScore = score;
          bestMatch = cmd;
        }
      });
      
      if (bestMatch) {
        this.executeVoiceCommand(bestMatch);
      } else {
        this.speak('Comando não reconhecido. Clique no ícone de ajuda para ver os comandos disponíveis.');
        this.recognitionMessage = 'Comando não reconhecido';
      }
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
    executeVoiceCommand(command) {
      console.log('Executando comando:', command);
      
      // Adiciona à história de navegação
      this.navigationHistory.push(command);
      if (this.navigationHistory.length > 10) {
        this.navigationHistory.shift();
      }
      
      const commandRoutes = {
        // Navegação geral
        "ir para início": "/dashboard/",
        "voltar": "history_back",
        "avançar": "history_forward",
        "rolar para baixo": "scroll_down", 
        "rolar para cima": "scroll_up",
        "atualizar página": "reload_page",
        
        // Comandos do sistema
        "abrir avaliações": "/painel_estudante/avaliacoes/",
        "abrir inscrições": "/painel_estudante/inscricoes/",
        "abrir matrículas": "/painel_estudante/matriculas/",
        "abrir faturas": "/painel_estudante/facturas/",
        "abrir mensalidades": "/painel_estudante/mensalidades/",
        "abrir vula": "/painel_estudante/vula/",
        "abrir perfil": "/painel_estudante/",
        "ir para painel": "/painel_estudante/",
        
        // Comandos de acessibilidade
        "ativar alto contraste": "toggle_high_contrast",
        "desativar alto contraste": "toggle_high_contrast",
        "aumentar fonte": "increase_font_size",
        "diminuir fonte": "decrease_font_size",
        "tamanho normal": "reset_font_size"
      };
      
      const action = commandRoutes[command];
      
      if (!action) {
        this.speak('Comando não encontrado');
        return;
      }
      
      // Executa ações especiais
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
          this.speak('Fonte restaurada ao tamanho normal');
          break;
          
        default:
          this.speak('Ação não reconhecida');
      }
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
      
      this.speak(`Abrindo ${pageName}`);
      
      // Navega após um pequeno delay
      setTimeout(() => {
        window.location.href = url;
      }, 1000);
    },

    // Ajustar tamanho da fonte
    adjustFontSize(factor) {
      const currentSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
      const newSize = Math.max(12, Math.min(24, currentSize * factor));
      document.documentElement.style.fontSize = newSize + 'px';
    },

    // Limpeza
    cleanup() {
      this.stopVoiceRecognition();
      this.stopReading();
      
      if (this.synthesis) {
        this.synthesis.cancel();
      }
    }
  }
}
</script>

<style scoped>
/* Animações */
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
    opacity: 0.5;
  }
}

/* Transições suaves */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Melhor contraste para acessibilidade */
.focus\:ring-4:focus {
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.5);
}

/* Alto contraste */
.high-contrast {
  filter: contrast(150%) brightness(120%);
}

.high-contrast * {
  text-shadow: 0 0 3px rgba(255,255,255,0.8) !important;
}
</style>