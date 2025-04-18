<!-- Navegacao por voz -->
<template>
    <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Comandos por Voz</span>
          <span class="text-sm text-gray-600 dark:text-gray-300">Navegue com sua voz</span>
        </div>
        <div class="flex items-center">
          <input 
            type="checkbox" 
            id="voice-commands" 
            :checked="voiceCommands" 
            @change="toggleVoiceCommands" 
            class="sr-only"
          >
          <div class="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': voiceCommands}">
            <div class="absolute left-1 top-1 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-7': voiceCommands}"></div>
          </div>
        </div>
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'VoiceNavigation',
    props: {
      voiceCommands: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        recognition: null
      }
    },
    watch: {
      voiceCommands: {
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
    },
    methods: {
      toggleVoiceCommands() {
        const newValue = !this.voiceCommands;
        this.$emit('update:voiceCommands', newValue);
      },
      
      startVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = true;
          this.recognition.lang = 'pt-BR';
          
          this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
            this.processVoiceCommand(transcript);
          };
          
          this.recognition.start();
          this.$emit('announce', 'Comandos de voz ativados');
        } else {
          alert('Seu navegador não suporta reconhecimento de voz.');
          this.$emit('update:voiceCommands', false);
        }
      },
      
      stopVoiceRecognition() {
        if (this.recognition) {
          this.recognition.stop();
          this.recognition = null;
          this.$emit('announce', 'Comandos de voz desativados');
        }
      },
      
      processVoiceCommand(command) {
        // Envia o comando para o componente pai para execução
        this.$emit('executeCommand', command);
      }
    }
  }
  </script>