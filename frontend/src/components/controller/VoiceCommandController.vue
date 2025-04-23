<!-- 
<template>
    <div v-if="active" class="fixed bottom-6 right-6 z-50 flex items-center bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-lg border border-gray-200 dark:border-gray-700">
      <div class="relative mr-2">
        <div class="w-3 h-3 rounded-full" :class="{'animate-pulse': isListening, 'bg-red-500': !isListening, 'bg-green-500': isListening}"></div>
      </div>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
        {{ isListening ? 'Ouvindo...' : 'Não está ouvindo' }}
      </span>
      
      Botão de informações
      <button 
        @click="toggleHelpMenu"
        class="ml-2 p-1 rounded-full text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        aria-label="Informações sobre comandos de voz"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    
    Menu de ajuda para comandos de voz
    <div 
      v-if="showHelpMenu && active" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white dark:bg-gray-900 rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] overflow-auto">
        <div class="p-4 bg-[#077b4b] mb-2">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-poppins text-white dark:text-white">
              Comandos de Voz Disponíveis
            </h2>
            <button 
              @click="toggleHelpMenu" 
              class="text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white rounded-full"
              aria-label="Fechar menu de ajuda"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="px-4 py-2">
          <div class="mb-4">
            <p class="text-gray-600 dark:text-gray-400 mb-2">Diga qualquer um destes comandos para navegar pelo sistema:</p>
          </div>
          
          Navegação Geral
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Navegação Geral</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in generalCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
          
          Comandos do Sistema
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Módulos do Sistema</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in systemCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
          
          Comandos de Acessibilidade
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Acessibilidade</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in accessibilityCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Dica: Você pode dizer "ajuda" a qualquer momento para ver estes comandos novamente.
          </p>
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
        errorCount: 0,
        lastCommand: '',
        recognitionTimeout: null,
        // Comandos disponíveis
        generalCommands: {
          "ir para início": "Navega para a página inicial",
          "voltar": "Retorna à página anterior",
          "avançar": "Avança para a próxima página",
          "rolar para baixo": "Rola a página para baixo",
          "rolar para cima": "Rola a página para cima",
          "ajuda": "Exibe esta lista de comandos disponíveis"
        },
        systemCommands: {
          "abrir avaliações": "Navega para o módulo de avaliações",
          "abrir inscrições": "Navega para o módulo de inscrições",
          "abrir matrículas": "Navega para o módulo de matrículas",
          "abrir faturas": "Navega para o módulo de faturas",
          "abrir mensalidades": "Navega para o módulo de mensalidades",
          "abrir vula": "Navega para o módulo Vula"
        },
        accessibilityCommands: {
          "ativar alto contraste": "Ativa o modo de alto contraste",
          "desativar alto contraste": "Desativa o modo de alto contraste",
          "aumentar fonte": "Aumenta o tamanho da fonte",
          "diminuir fonte": "Diminui o tamanho da fonte",
          "tamanho normal": "Retorna a fonte ao tamanho normal"
        }
      }
    },
    watch: {
      active: {
        immediate: true,
        handler(newValue) {
          if (newValue) {
            this.startVoiceRecognition();
          } else if (this.recognition) {
            this.stopVoiceRecognition();
          }
        }
      }
    },
    beforeUnmount() {
      this.stopVoiceRecognition();
      clearTimeout(this.recognitionTimeout);
    },
    methods: {
      toggleHelpMenu() {
        this.showHelpMenu = !this.showHelpMenu;
      },
      
      startVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = true;
          this.recognition.interimResults = false;
          this.recognition.lang = 'pt-BR';
          
          this.recognition.onstart = () => {
            this.isListening = true;
            this.$emit('announce', 'Comandos de voz ativados');
          };
          
          this.recognition.onend = () => {
            this.isListening = false;
            
            // Reinicia automaticamente o reconhecimento se os comandos de voz ainda estiverem ativados
            if (this.active) {
              this.recognitionTimeout = setTimeout(() => {
                this.startVoiceRecognition();
              }, 500);
            }
          };
          
          this.recognition.onerror = (event) => {
            console.error('Erro de reconhecimento de voz:', event.error);
            this.errorCount++;
            
            // Se houver muitos erros consecutivos, notificar o usuário
            if (this.errorCount > 3) {
              this.$emit('announce', 'Estamos tendo dificuldades em reconhecer sua voz. Por favor, verifique seu microfone.');
              this.errorCount = 0;
            }
          };
          
          this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            
            // Evita processar o mesmo comando várias vezes
            if (transcript !== this.lastCommand) {
              this.lastCommand = transcript;
              this.processVoiceCommand(transcript);
            }
          };
          
          this.recognition.start();
        } else {
          console.error('Seu navegador não suporta reconhecimento de voz.');
          this.$emit('announce', 'Seu navegador não suporta reconhecimento de voz.');
        }
      },
      
      stopVoiceRecognition() {
        if (this.recognition) {
          this.recognition.stop();
          this.recognition = null;
          this.isListening = false;
          this.$emit('announce', 'Comandos de voz desativados');
        }
        clearTimeout(this.recognitionTimeout);
      },
      
      processVoiceCommand(command) {
        console.log('Comando recebido:', command);
        
        // Comando de ajuda
        if (command.includes('ajuda')) {
          this.showHelpMenu = true;
          this.$emit('announce', 'Exibindo lista de comandos disponíveis');
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
          this.$emit('executeCommand', bestMatch);
          this.$emit('announce', `Executando comando: ${bestMatch}`);
        } else {
          // Se não encontrou correspondência, informa o usuário
          this.$emit('announce', 'Comando não reconhecido. Diga "ajuda" para ver os comandos disponíveis.');
        }
      },
      
      // Função simples para calcular similaridade entre strings (para reconhecimento aproximado)
      getSimilarityScore(str1, str2) {
        str1 = str1.toLowerCase();
        str2 = str2.toLowerCase();
        
        // Verifica se uma string contém a outra
        if (str1.includes(str2) || str2.includes(str1)) {
          return 0.9;
        }
        
        // Verifica palavras em comum
        const words1 = str1.split(' ');
        const words2 = str2.split(' ');
        
        let commonWords = 0;
        words1.forEach(word => {
          if (words2.includes(word) && word.length > 2) { // Ignora palavras muito curtas
            commonWords++;
          }
        });
        
        const totalWords = Math.max(words1.length, words2.length);
        return commonWords / totalWords;
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
  </style> -->


  <template>
    <div v-if="active" class="fixed inset-x-0 bottom-6 mx-auto w-fit z-50 flex items-center bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-lg border border-gray-200 dark:border-gray-700">
      <div class="relative mr-2">
        <div class="w-3 h-3 rounded-full" :class="{'animate-pulse': isListening, 'bg-red-500': !isListening, 'bg-green-500': isListening}"></div>
      </div>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
        {{ isListening ? 'Ouvindo...' : 'Não está ouvindo' }}
      </span>
      
      <!-- Botão de informações -->
      <button 
        @click="toggleHelpMenu"
        class="ml-2 p-1 rounded-full text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        aria-label="Informações sobre comandos de voz"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    
    <!-- Menu de ajuda para comandos de voz -->
    <div 
      v-if="showHelpMenu && active" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white dark:bg-gray-900 rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] overflow-auto">
        <div class="p-4 bg-[#077b4b] mb-2">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-poppins text-white dark:text-white">
              Comandos de Voz Disponíveis
            </h2>
            <button 
              @click="toggleHelpMenu" 
              class="text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white rounded-full"
              aria-label="Fechar menu de ajuda"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="px-4 py-2">
          <div class="mb-4">
            <p class="text-gray-600 dark:text-gray-400 mb-2">Diga qualquer um destes comandos para navegar pelo sistema:</p>
          </div>
          
          <!-- Navegação Geral -->
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Navegação Geral</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in generalCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
          
          <!-- Comandos do Sistema -->
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Módulos do Sistema</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in systemCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
          
          <!-- Comandos de Acessibilidade -->
          <div class="mb-4">
            <h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 border-b border-gray-200 dark:border-gray-700 pb-1">Acessibilidade</h3>
            <ul class="space-y-2">
              <li v-for="(desc, cmd) in accessibilityCommands" :key="cmd" class="flex">
                <span class="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white px-2 py-1 rounded font-mono text-sm min-w-[150px] mr-2">{{ cmd }}</span>
                <span class="text-gray-600 dark:text-gray-400">{{ desc }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Dica: Você pode dizer "ajuda" a qualquer momento para ver estes comandos novamente.
          </p>
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
        errorCount: 0,
        lastCommand: '',
        recognitionTimeout: null,
        // Comandos disponíveis
        generalCommands: {
          "ir para início": "Navega para a página inicial",
          "voltar": "Retorna à página anterior",
          "avançar": "Avança para a próxima página",
          "rolar para baixo": "Rola a página para baixo",
          "rolar para cima": "Rola a página para cima",
          "ajuda": "Exibe esta lista de comandos disponíveis"
        },
        systemCommands: {
          "abrir avaliações": "Navega para o módulo de avaliações",
          "abrir inscrições": "Navega para o módulo de inscrições",
          "abrir matrículas": "Navega para o módulo de matrículas",
          "abrir faturas": "Navega para o módulo de faturas",
          "abrir mensalidades": "Navega para o módulo de mensalidades",
          "abrir vula": "Navega para o módulo Vula"
        },
        accessibilityCommands: {
          "ativar alto contraste": "Ativa o modo de alto contraste",
          "desativar alto contraste": "Desativa o modo de alto contraste",
          "aumentar fonte": "Aumenta o tamanho da fonte",
          "diminuir fonte": "Diminui o tamanho da fonte",
          "tamanho normal": "Retorna a fonte ao tamanho normal"
        }
      }
    },
    watch: {
      active: {
        immediate: true,
        handler(newValue) {
          if (newValue) {
            this.startVoiceRecognition();
          } else if (this.recognition) {
            this.stopVoiceRecognition();
          }
        }
      }
    },
    beforeUnmount() {
      this.stopVoiceRecognition();
      clearTimeout(this.recognitionTimeout);
    },
    methods: {
      toggleHelpMenu() {
        this.showHelpMenu = !this.showHelpMenu;
      },
      
      startVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = true;
          this.recognition.interimResults = false;
          this.recognition.lang = 'pt-BR';
          
          this.recognition.onstart = () => {
            this.isListening = true;
            this.$emit('announce', 'Comandos de voz ativados');
          };
          
          this.recognition.onend = () => {
            this.isListening = false;
            
            // Reinicia automaticamente o reconhecimento se os comandos de voz ainda estiverem ativados
            if (this.active) {
              this.recognitionTimeout = setTimeout(() => {
                this.startVoiceRecognition();
              }, 500);
            }
          };
          
          this.recognition.onerror = (event) => {
            console.error('Erro de reconhecimento de voz:', event.error);
            this.errorCount++;
            
            // Se houver muitos erros consecutivos, notificar o usuário
            if (this.errorCount > 3) {
              this.$emit('announce', 'Estamos tendo dificuldades em reconhecer sua voz. Por favor, verifique seu microfone.');
              this.errorCount = 0;
            }
          };
          
          this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            
            // Evita processar o mesmo comando várias vezes
            if (transcript !== this.lastCommand) {
              this.lastCommand = transcript;
              this.processVoiceCommand(transcript);
            }
          };
          
          this.recognition.start();
        } else {
          console.error('Seu navegador não suporta reconhecimento de voz.');
          this.$emit('announce', 'Seu navegador não suporta reconhecimento de voz.');
        }
      },
      
      stopVoiceRecognition() {
        if (this.recognition) {
          this.recognition.stop();
          this.recognition = null;
          this.isListening = false;
          this.$emit('announce', 'Comandos de voz desativados');
        }
        clearTimeout(this.recognitionTimeout);
      },
      
      processVoiceCommand(command) {
        console.log('Comando recebido:', command);
        
        // Comando de ajuda
        if (command.includes('ajuda')) {
          this.showHelpMenu = true;
          this.$emit('announce', 'Exibindo lista de comandos disponíveis');
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
          this.$emit('executeCommand', bestMatch);
          this.$emit('announce', `Executando comando: ${bestMatch}`);
        } else {
          // Se não encontrou correspondência, informa o usuário
          this.$emit('announce', 'Comando não reconhecido. Diga "ajuda" para ver os comandos disponíveis.');
        }
      },
      
      // Função simples para calcular similaridade entre strings (para reconhecimento aproximado)
      getSimilarityScore(str1, str2) {
        str1 = str1.toLowerCase();
        str2 = str2.toLowerCase();
        
        // Verifica se uma string contém a outra
        if (str1.includes(str2) || str2.includes(str1)) {
          return 0.9;
        }
        
        // Verifica palavras em comum
        const words1 = str1.split(' ');
        const words2 = str2.split(' ');
        
        let commonWords = 0;
        words1.forEach(word => {
          if (words2.includes(word) && word.length > 2) { // Ignora palavras muito curtas
            commonWords++;
          }
        });
        
        const totalWords = Math.max(words1.length, words2.length);
        return commonWords / totalWords;
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
  </style>