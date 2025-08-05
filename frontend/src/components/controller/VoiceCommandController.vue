<template>
  <div v-if="showComponent">
    <div class="fixed inset-x-0 bottom-6 mx-auto z-50 flex items-center bg-white dark:bg-gray-800 rounded-lg p-4 shadow-lg border border-gray-200 dark:border-gray-700 w-full max-w-xl justify-between">
      <div class="flex items-center space-x-4 flex-grow">
        <!-- Botão de microfone clicável para ativar/desativar -->
        <button 
          @click="toggleRecognition"
          class="relative w-10 h-10 rounded-full flex items-center justify-center transition-colors"
          :class="isListening ? 'bg-[#4A90E2] dark:bg-[#4A90E2]' : 'bg-[#2060a9] dark:bg-[#2060a9]'"
          aria-label="Alternar reconhecimento de voz"
        >
          <div v-if="!isListening" class="absolute w-8 h-0.5 bg-white rotate-45 rounded-full"></div>
          <div v-if="recognitionState === 'listening'" class="w-3 h-3 absolute top-0 right-0 rounded-full bg-[#4A90E2] animate-pulse"></div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </button>

        <!-- Status do microfone com largura fixa -->
        <div 
          class="p-2 rounded-full text-white w-full max-w-xl"
          :class="isListening ? 'bg-[#2060a9] dark:bg-[#2060a9]' : 'bg-[#2060a9] dark:bg-[#2060a9]'"
        >
          <span class="font-medium text-white px-2">
            {{ statusMessage }}
          </span>
          <p v-if="lastTranscript" class="text-sm text-blue-200 mt-1 truncate px-2">
            {{ lastTranscript }}
          </p>
        </div>
      </div>

      <!-- Botão de informações no canto direito -->
      <button 
        @click="toggleHelpMenu"
        class="ml-4 p-2 rounded-full text-white hover:bg-[#4A90E2] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4A90E2] transition-colors bg-[#4A90E2]"
        aria-label="Informações sobre comandos de voz"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
      </button>
    </div>

    <!-- Modal de ajuda para comandos de voz -->
    <div 
      v-if="showHelpMenu" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
    >
      <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] overflow-hidden flex flex-col">
        <!-- Header -->
        <div class="p-6 bg-gradient-to-r from-[#4A90E2] to-[#2060a9] dark:from-[#2060a9] dark:to-[#233e5c]">
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
              @click="toggleHelpMenu" 
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
            <h3 class="text-lg font-bold text-[#4A90E2] dark:text-[#72aae9] mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
              Navegação Geral
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="(desc, cmd) in generalCommands" :key="cmd" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-200 dark:border-blue-700 hover:shadow-md transition-shadow">
                <div class="font-mono text-sm bg-blue-50 dark:bg-[#2060a9] text-[#2060a9] dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
                  {{ cmd }}
                </div>
                <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
                  {{ desc }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Comandos do Sistema -->
          <div class="mb-6">
            <h3 class="text-lg font-bold text-[#4A90E2] dark:text-[#72aae9]  mb-3 border-b border-blue-200 dark:border-blue-700 pb-2">
              Páginas do Sistema
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="(desc, cmd) in systemCommands" :key="cmd" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
                <div class="font-mono text-sm bg-blue-50 dark:bg-blue-700 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
                  {{ cmd }}
                </div>
                <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
                  {{ desc }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Comandos de Acessibilidade -->
          <div class="mb-6">
            <h3 class="text-lg font-bold text-[#4A90E2] dark:text-[#72aae9]  mb-3 border-b border-blue-200 dark:border-emerald-700 pb-2">
              Acessibilidade
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="(desc, cmd) in accessibilityCommands" :key="cmd" class="flex flex-col md:flex-row bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-blue-100 dark:border-blue-700 hover:shadow-md transition-shadow">
                <div class="font-mono text-sm bg-blue-50 dark:bg-blue-700 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-md mb-2 md:mb-0 md:mr-3 flex-shrink-0 md:w-auto w-full">
                  {{ cmd }}
                </div>
                <div class="text-gray-700 dark:text-gray-300 text-sm md:text-base flex items-center">
                  {{ desc }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-blue-50 dark:bg-emerald-950">
          <div class="flex items-center justify-between">
            <p class="text-sm text-[#5194e0] dark:text-[#72aae9] ">
              <span class="font-bold">Dica:</span> Você pode dizer "ajuda" a qualquer momento para ver estes comandos novamente.
            </p>
            <button 
              @click="toggleHelpMenu"
              class="px-4 py-2 bg-[#4A90E2] hover:bg-[#2060a9] text-white rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:ring-offset-2"
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
      isListening: false,
      showHelpMenu: false,
      showComponent: false, // Controla se o componente deve ser exibido ou não
      errorCount: 0,
      lastCommand: '',
      lastTranscript: '',
      recognitionMessage: '',
      recognitionState: 'silenced', // 'listening', 'silenced', 'thinking', 'error'
      initDelay: 1500, // Delay para inicializar o reconhecimento após ativação
      recognitionTimeout: null,
      stateDisplayTimeout: null,
      lastErrorTime: 0, // Para evitar spam de erros
      // Comandos disponíveis
      generalCommands: {
        "ir para início": "Navega para a página inicial",
        "voltar": "Retorna à página anterior",
        "avançar": "Avança para a próxima página",
        "rolar para baixo": "Rola a página para baixo",
        "rolar para cima": "Rola a página para cima",
        "actualizar página": "Recarrega a página actual",
        "fechar": "Fecha a janela ou diálogo actual",
        "maximizar": "Maximiza a janela atual",
        "minimizar": "Minimiza a janela atual",
        "ajuda": "Exibe esta lista de comandos disponíveis"
      },
      systemCommands: {
        "abrir avaliações": "Navega para a página de avaliações",
        "abrir inscrições": "Navega para a página de inscrições",
        "abrir matrículas": "Navega para a página de matrículas",
        "abrir facturas": "Navega para a página de facturas",
        "abrir mensalidades": "Navega para a página de mensalidades",
        "abrir vula": "Navega para a página Vula",
        "abrir perfil": "Acede ao perfil do utilizador",
        "abrir configurações": "Acede às configurações do sistema",
      },
      accessibilityCommands: {
        "activar alto contraste": "Activa o modo de alto contraste",
        "desactivar alto contraste": "Desactiva o modo de alto contraste",
        "aumentar fonte": "Aumenta o tamanho da fonte",
        "diminuir fonte": "Diminui o tamanho da fonte",
        "tamanho normal": "Retorna a fonte ao tamanho normal",
        "activar leitor de ecra": "Activa o leitor de ecra",
        "desactivar leitor de ecra": "Desactiva o leitor de ecra",
        "modo normal": "Retorna ao modo de visualização padrão",
      }
    }
  },
  computed: {
    statusMessage() {
      switch(this.recognitionState) {
        case 'listening':
          return 'Ouvindo...';
        case 'thinking':
          return 'Processando comando...';
        case 'error':
          return `Erro: ${this.recognitionMessage}`;
        case 'silenced':
          return this.isListening ? 'Clique no microfone para desactivar' : 'Clique no microfone para activar';
        default:
          return 'Aguardando...';
      }
    }
  },
  watch: {
    active: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.showComponent = true; // Mostra o componente quando ativado no menu
        } else {
          this.stopVoiceRecognition();
          this.showComponent = false; // Esconde o componente quando desativado no menu
        }
      }
    }
  },
  beforeUnmount() {
    this.stopVoiceRecognition();
    clearTimeout(this.recognitionTimeout);
    clearTimeout(this.stateDisplayTimeout);
  },
  methods: {
    toggleHelpMenu() {
      this.showHelpMenu = !this.showHelpMenu;
    },
    
    // Método para alternar o reconhecimento de voz
    toggleRecognition() {
      if (this.isListening) {
        this.stopVoiceRecognition();
      } else {
        this.startVoiceRecognition();
      }
    },
    
    startVoiceRecognition() {
      if (!this.active) {
        this.$emit('announce', 'Os comandos de voz estão desativados no sistema');
        return;
      }
      
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        try {
          // Para qualquer instância de reconhecimento existente primeiro
          if (this.recognition) {
            try {
              this.recognition.stop();
            } catch (e) {
              console.error("Erro ao parar instância anterior de reconhecimento:", e);
            }
          }
          
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = true;
          this.recognition.interimResults = false;
          this.recognition.lang = 'pt-BR';
          
          // Ajusta configurações para melhorar a precisão
          this.recognition.maxAlternatives = 3;
          
          this.recognition.onstart = () => {
            this.isListening = true;
            this.recognitionState = 'listening';
            this.$emit('announce', 'Comandos de voz ativados');
          };
          
          this.recognition.onend = () => {
            // Se o estado ainda não for 'silenced', significa que o reconhecimento foi encerrado por um erro
            // ou terminou naturalmente, não por uma ação do usuário
            if (this.recognitionState !== 'silenced' && this.isListening) {
              // Tenta reiniciar após um breve delay
              this.recognitionTimeout = setTimeout(() => {
                if (this.isListening && this.active) {
                  try {
                    this.recognition.start();
                  } catch (e) {
                    console.error("Erro ao reiniciar reconhecimento:", e);
                    this.isListening = false;
                    this.recognitionState = 'error';
                    this.recognitionMessage = 'Falha ao reiniciar o reconhecimento';
                  }
                }
              }, 1000);
            }
          };
          
          this.recognition.onerror = (event) => {
            const now = Date.now();
            
            // Trata o erro "aborted" de forma diferente - geralmente não é um erro real
            if (event.error === 'aborted') {
              console.log("Reconhecimento abortado, será reiniciado se ainda estiver ativo");
              return; // Não trata como erro, deixa o manipulador onend reiniciá-lo
            }
            
            // Ignora erros muito frequentes (menos de 2 segundos entre eles)
            if (now - this.lastErrorTime < 2000) {
              return;
            }
            
            this.lastErrorTime = now;
            console.error('Erro de reconhecimento de voz:', event.error);
            
            // Não incrementa o contador de erros em caso de "no-speech"
            if (event.error !== 'no-speech') {
              this.errorCount++;
            }
            
            if (event.error === 'network') {
              this.recognitionMessage = 'Verifique sua conexão de internet';
            } else if (event.error === 'not-allowed') {
              this.recognitionMessage = 'Permissão de microfone negada';
            } else if (event.error === 'no-speech') {
              // Não mostra mensagem para "no-speech"
              return;
            } else {
              this.recognitionMessage = 'Fala não reconhecida';
            }
            
            this.recognitionState = 'error';
            
            // Se houver muitos erros consecutivos, notificar o usuário
            if (this.errorCount > 3) {
              this.$emit('announce', 'Estamos tendo dificuldades em reconhecer sua voz. Por favor, verifique seu microfone.');
              this.errorCount = 0;
            }
          };
          
          this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            this.lastTranscript = transcript;
            this.recognitionState = 'thinking';
            
            // Evita processar o mesmo comando várias vezes
            if (transcript !== this.lastCommand) {
              this.lastCommand = transcript;
              this.processVoiceCommand(transcript);
            }
            
            // Após processar, volta ao estado de escuta
            setTimeout(() => {
              if (this.recognitionState === 'thinking') {
                this.recognitionState = 'listening';
              }
            }, 2000);
          };
          
          // Adiciona um pequeno delay antes de iniciar para evitar ciclos rápidos de início/parada
          setTimeout(() => {
            try {
              this.recognition.start();
            } catch (e) {
              console.error("Erro ao iniciar reconhecimento:", e);
              this.isListening = false;
              this.recognitionState = 'error';
              this.recognitionMessage = 'Falha ao iniciar o reconhecimento';
            }
          }, 500);
        } catch (error) {
          console.error('Erro ao inicializar o reconhecimento de voz:', error);
          this.$emit('announce', 'Erro ao inicializar o reconhecimento de voz');
          this.isListening = false;
          this.recognitionState = 'error';
          this.recognitionMessage = 'Falha ao inicializar';
        }
      } else {
        console.error('Seu navegador não suporta reconhecimento de voz.');
        this.$emit('announce', 'Seu navegador não suporta reconhecimento de voz.');
        this.recognitionState = 'error';
        this.recognitionMessage = 'Navegador incompatível';
      }
    },
    
    stopVoiceRecognition() {
      if (this.recognition) {
        try {
          this.recognition.stop();
        } catch (e) {
          console.error('Erro ao parar reconhecimento:', e);
        }
        this.recognition = null;
      }
      
      this.isListening = false;
      this.recognitionState = 'silenced';
      this.$emit('announce', 'Comandos de voz desativados');
      
      // Limpa todos os timeouts
      if (this.recognitionTimeout) {
        clearTimeout(this.recognitionTimeout);
        this.recognitionTimeout = null;
      }
      
      if (this.stateDisplayTimeout) {
        clearTimeout(this.stateDisplayTimeout);
        this.stateDisplayTimeout = null;
      }
    },
    
    processVoiceCommand(command) {
      console.log('Comando recebido:', command);
      
      // Comando de ajuda
      if (command.includes('ajuda')) {
        this.showHelpMenu = true;
        this.$emit('announce', 'Exibindo lista de comandos disponíveis');
        return;
      }
      
      // Tratamento para comandos específicos de ativação/desativação do reconhecimento
      if (command.includes('desativar microfone') || command.includes('parar de ouvir') || command.includes('desligar microfone')) {
        this.stopVoiceRecognition();
        return;
      }
      
      // Verifica todos os comandos disponíveis
      const allCommands = {
        ...this.generalCommands,
        ...this.systemCommands,
        ...this.accessibilityCommands
      };
      
      // Procura por correspondências aproximadas nos comandos
      let bestMatch = null;
      let bestScore = 0;
      
      Object.keys(allCommands).forEach(cmd => {
        const score = this.getSimilarityScore(command, cmd);
        if (score > bestScore && score > 0.7) { // Threshold de 70% de similaridade
          bestScore = score;
          bestMatch = cmd;
        }
      });
      
      if (bestMatch) {
        // Se encontrou uma correspondência, executa o comando
        this.recognitionMessage = `Executando: ${bestMatch}`;
        this.$emit('executeCommand', bestMatch);
        this.$emit('announce', `Executando comando: ${bestMatch}`);
      } else {
        // Se não encontrou correspondência, informa o usuário
        this.recognitionMessage = 'Comando não reconhecido';
        this.$emit('announce', 'Comando não reconhecido. Diga "ajuda" para ver os comandos disponíveis.');
      }
    },
    
    // Função melhorada para calcular similaridade entre strings
    getSimilarityScore(str1, str2) {
      str1 = str1.toLowerCase().trim();
      str2 = str2.toLowerCase().trim();
      
      // Verifica se uma string contém a outra
      if (str1.includes(str2)) {
        return 0.9;
      }
      
      if (str2.includes(str1)) {
        return 0.8;
      }
      
      // Verifica palavras em comum
      const words1 = str1.split(/\s+/);
      const words2 = str2.split(/\s+/);
      
      let commonWords = 0;
      let significantWords = 0;
      
      words1.forEach(word => {
        if (word.length > 2) { // Ignora palavras muito curtas
          significantWords++;
          if (words2.includes(word)) {
            commonWords++;
          }
        }
      });
      
      if (significantWords === 0) return 0;
      return commonWords / significantWords;
    }
  }
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
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
  transition-duration: 150ms;
}

.transition-shadow {
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>