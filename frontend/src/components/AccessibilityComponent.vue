<template>
    <div>
      <!-- Skip link for accessibility -->
      <a href="#main-content" class="absolute -left-[9999px] top-auto w-px h-px overflow-hidden focus:fixed focus:top-0 focus:left-0 focus:w-auto focus:h-auto focus:p-2 focus:bg-white focus:text-black focus:font-bold focus:z-50 focus:shadow-lg focus:no-underline">
        Pular para o conteúdo principal
      </a>
  
      <!-- Accessibility button -->
      <button 
        @click="toggleMenu"
        class="fixed bottom-32 left-0 bg-green-700 hover:bg-green-600 text-white py-4 px-6 rounded-r-full shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 z-50 group"
        aria-label="Opcoes de acessibilidade"
      >
          <img src="/static/core/img/accessibility_icon.png" alt="Icone de acessibilidade" class="h-8 w-8 brightness-0 invert">
        
        <div class="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2 bg-gray-800 text-white text-sm rounded whitespace-nowrap invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-opacity duration-300 z-50">
          <div class="absolute top-1/2 right-full -mt-1 border-solid border-8 border-transparent border-r-gray-800"></div>
          Clique para opcoes de acessibilidade
        </div>
      </button>
  
      <!-- Accessibility menu -->
      <div 
        v-if="isOpen" 
        class="fixed bottom-32 left-0 bg-white dark:bg-gray-900 rounded-lg shadow-xl p-5 w-80 border border-gray-200 dark:border-gray-700 z-40 transition-all duration-300"
        role="dialog"
        aria-labelledby="accessibility-title"
      >
        <!-- Header with logos -->
        <div class="flex items-center justify-between mb-4 border-b pb-3 border-gray-200 dark:border-gray-700">
          <div class="flex items-center space-x-3">
            <img src="/static/core/img/uem_logo.png" alt="Logo UEM" class="h-8">
            <div class="border-l border-gray-300 dark:border-gray-600 h-8"></div>
            <img src="/static/core/img/siga_logo.png" alt="Logo SIGA" class="h-6">
          </div>
          
          <button 
            @click="toggleMenu" 
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 p-1 rounded-full"
            aria-label="Fechar menu de acessibilidade"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <h2 id="accessibility-title" class="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-green-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Acessibilidade SIGA
        </h2>
        
        <div class="space-y-5">
          <!-- Font size control -->
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
            <h3 class="font-medium text-gray-800 dark:text-gray-200 mb-3 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
              </svg>
              Tamanho da Fonte
            </h3>
            <div class="flex items-center justify-between">
              <button 
                @click="decreaseFont" 
                class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-4 py-2 rounded-lg font-bold shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                aria-label="Diminuir fonte"
              >
                A-
              </button>
              <div class="text-center">
                <span class="text-sm text-gray-600 dark:text-gray-300 block">Tamanho</span>
                <span class="font-medium text-gray-800 dark:text-white">{{ fontSize }}</span>
              </div>
              <button 
                @click="increaseFont" 
                class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-4 py-2 rounded-lg font-bold shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                aria-label="Aumentar fonte"
              >
                A+
              </button>
            </div>
          </div>
          
          <!-- High contrast control -->
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
            <label class="flex items-center cursor-pointer">
              <div class="flex-shrink-0 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <div class="flex-grow">
                <span class="block text-gray-800 dark:text-white font-medium">Alto Contraste</span>
                <span class="text-sm text-gray-600 dark:text-gray-300">Melhora visualização de textos</span>
              </div>
              <div class="flex items-center">
                <input 
                  type="checkbox" 
                  id="high-contrast" 
                  v-model="highContrast" 
                  @change="toggleContrast" 
                  class="sr-only"
                >
                <div class="relative w-12 h-6 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': highContrast}">
                  <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-6': highContrast}"></div>
                </div>
              </div>
            </label>
          </div>
          
          <!-- Screen reader -->
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
            <label class="flex items-center cursor-pointer">
              <div class="flex-shrink-0 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </div>
              <div class="flex-grow">
                <span class="block text-gray-800 dark:text-white font-medium">Leitor de Tela</span>
                <span class="text-sm text-gray-600 dark:text-gray-300">Narração de conteúdos</span>
              </div>
              <div class="flex items-center">
                <input 
                  type="checkbox" 
                  id="screen-reader" 
                  v-model="screenReader" 
                  @change="toggleScreenReader" 
                  class="sr-only"
                >
                <div class="relative w-12 h-6 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': screenReader}">
                  <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-6': screenReader}"></div>
                </div>
              </div>
            </label>
          </div>
          
          <!-- Voice commands -->
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
            <label class="flex items-center cursor-pointer">
              <div class="flex-shrink-0 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="flex-grow">
                <span class="block text-gray-800 dark:text-white font-medium">Comandos por Voz</span>
                <span class="text-sm text-gray-600 dark:text-gray-300">Navegue com sua voz</span>
              </div>
              <div class="flex items-center">
                <input 
                  type="checkbox" 
                  id="voice-commands" 
                  v-model="voiceCommands" 
                  @change="toggleVoiceCommands" 
                  class="sr-only"
                >
                <div class="relative w-12 h-6 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': voiceCommands}">
                  <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-6': voiceCommands}"></div>
                </div>
              </div>
            </label>
          </div>
          
          <!-- Cursor section -->
          <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
            <div class="flex items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
              </svg>
              <h3 class="font-medium text-gray-800 dark:text-white">Cursor</h3>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Amplie o cursor e altere a sua cor</p>
            <div class="flex gap-2">
              <button 
                @click="setCursorColor('white')" 
                class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium"
                :class="cursorColor === 'white' ? 'ring-2 ring-green-500 bg-white text-black' : 'bg-white text-black'"
              >
                BRANCO
              </button>
              <button 
                @click="setCursorColor('black')" 
                class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium"
                :class="cursorColor === 'black' ? 'ring-2 ring-green-500 bg-gray-900 text-white' : 'bg-gray-900 text-white'"
              >
                PRETO
              </button>
            </div>
          </div>
        </div>
        
        <div class="mt-5 pt-3 border-t border-gray-200 dark:border-gray-700">
          <button 
            @click="resetSettings" 
            class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-800 dark:text-white py-3 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center justify-center"
            aria-label="Restaurar configurações padrão"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Restaurar Configurações Padrão
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AccessibilityComponent',
    data() {
      return {
        isOpen: false,
        fontSize: 'Normal',
        highContrast: false,
        screenReader: false,
        voiceCommands: false,
        cursorColor: 'black',
        recognition: null
      }
    },
    mounted() {
      this.loadSettings();
      window.addEventListener('keydown', this.handleKeyDown);
      
      // Add cursor styles
      this.addCursorStyles();
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.handleKeyDown);
      if (this.recognition) {
        this.recognition.stop();
      }
    },
    methods: {
      toggleMenu() {
        this.isOpen = !this.isOpen;
      },
      
      increaseFont() {
        const body = document.body;
        const currentSize = window.getComputedStyle(body).fontSize;
        const newSize = parseFloat(currentSize) * 1.1;
        body.style.fontSize = `${newSize}px`;
        this.fontSize = 'Grande';
        this.saveSettings();
        
        this.announceToScreenReader('Tamanho da fonte aumentado');
      },
      
      decreaseFont() {
        const body = document.body;
        const currentSize = window.getComputedStyle(body).fontSize;
        const newSize = parseFloat(currentSize) * 0.9;
        body.style.fontSize = `${newSize}px`;
        this.fontSize = 'Pequeno';
        this.saveSettings();
        
        this.announceToScreenReader('Tamanho da fonte diminuído');
      },
      
      toggleContrast() {
        if (this.highContrast) {
          document.body.classList.add('high-contrast');
          document.documentElement.style.setProperty('--bg-color', '#000');
          document.documentElement.style.setProperty('--text-color', '#fff');
          document.body.classList.add('high-contrast-mode');
          
          this.announceToScreenReader('Alto contraste ativado');
        } else {
          document.body.classList.remove('high-contrast');
          document.documentElement.style.removeProperty('--bg-color');
          document.documentElement.style.removeProperty('--text-color');
          document.body.classList.remove('high-contrast-mode');
          
          this.announceToScreenReader('Alto contraste desativado');
        }
        this.saveSettings();
      },
      
      toggleScreenReader() {
        this.announceToScreenReader(
          this.screenReader ? 'Leitor de tela ativado' : 'Leitor de tela desativado'
        );
        this.saveSettings();
      },
      
      toggleVoiceCommands() {
        if (this.voiceCommands) {
          this.startVoiceRecognition();
        } else {
          this.stopVoiceRecognition();
        }
        this.saveSettings();
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
          this.announceToScreenReader('Comandos de voz ativados');
        } else {
          alert('Seu navegador não suporta reconhecimento de voz.');
          this.voiceCommands = false;
        }
      },
      
      stopVoiceRecognition() {
        if (this.recognition) {
          this.recognition.stop();
          this.recognition = null;
          this.announceToScreenReader('Comandos de voz desativados');
        }
      },
      
      processVoiceCommand(command) {
        if (command.includes('aumentar fonte') || command.includes('aumentar tamanho')) {
          this.increaseFont();
        } else if (command.includes('diminuir fonte') || command.includes('diminuir tamanho')) {
          this.decreaseFont();
        } else if (command.includes('alto contraste')) {
          this.toggleContrast();
        } else if (command.includes('resetar') || command.includes('restaurar')) {
          this.resetSettings();
        } else if (command.includes('fechar menu')) {
          this.isOpen = false;
        } else if (command.includes('cursor branco')) {
          this.setCursorColor('white');
        } else if (command.includes('cursor preto')) {
          this.setCursorColor('black');
        }
      },
      
      setCursorColor(color) {
        this.cursorColor = color;
        document.body.classList.remove('cursor-color-black', 'cursor-color-white');
        document.body.classList.add(`cursor-color-${color}`);
        localStorage.setItem('accessibilityCursorColor', color);
      },
      
      resetSettings() {
        // Reset font size
        document.body.style.fontSize = '';
        this.fontSize = 'Normal';
        
        // Reset contrast
        this.highContrast = false;
        document.body.classList.remove('high-contrast');
        document.body.classList.remove('high-contrast-mode');
        document.documentElement.style.removeProperty('--bg-color');
        document.documentElement.style.removeProperty('--text-color');
        
        // Reset screen reader
        this.screenReader = false;
        
        // Reset voice commands
        if (this.voiceCommands) {
          this.stopVoiceRecognition();
        }
        this.voiceCommands = false;
        
        // Reset cursor
        this.cursorColor = 'black';
        document.body.classList.remove('cursor-color-white');
        document.body.classList.add('cursor-color-black');
        
        this.saveSettings();
        this.announceToScreenReader('Configurações restauradas para o padrão');
      },
      
      saveSettings() {
        const settings = {
          fontSize: this.fontSize,
          highContrast: this.highContrast,
          screenReader: this.screenReader,
          voiceCommands: this.voiceCommands,
          cursorColor: this.cursorColor
        };
        
        localStorage.setItem('accessibility_settings', JSON.stringify(settings));
      },
      
      loadSettings() {
        const savedSettings = localStorage.getItem('accessibility_settings');
        if (savedSettings) {
          const settings = JSON.parse(savedSettings);
          this.fontSize = settings.fontSize || 'Normal';
          this.highContrast = settings.highContrast || false;
          this.screenReader = settings.screenReader || false;
          this.voiceCommands = settings.voiceCommands || false;
          this.cursorColor = settings.cursorColor || 'black';
          
          // Apply settings
          if (this.highContrast) {
            this.toggleContrast();
          }
          
          if (this.fontSize !== 'Normal') {
            const factor = this.fontSize === 'Grande' ? 1.1 : 0.9;
            const body = document.body;
            const defaultSize = '16px';
            const currentSize = parseFloat(defaultSize);
            body.style.fontSize = `${currentSize * factor}px`;
          }
          
          if (this.voiceCommands) {
            this.startVoiceRecognition();
          }
          
          // Apply cursor color
          document.body.classList.add(`cursor-color-${this.cursorColor}`);
        }
      },
      
      announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'assertive');
        announcement.setAttribute('class', 'sr-only');
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
          document.body.removeChild(announcement);
        }, 3000);
      },
      
      handleKeyDown(event) {
        if (event.altKey && event.key === 'a') {
          this.toggleMenu();
          event.preventDefault();
        }
      },
      
      addCursorStyles() {
        // Add style element for cursor styling
        const styleEl = document.createElement('style');
        styleEl.innerHTML = `
          .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
          }
          
          body.high-contrast-mode {
            background-color: #000 !important;
            color: #fff !important;
          }
          
          body.high-contrast-mode a {
            color: #ffff00 !important;
          }
          
          body.high-contrast-mode button,
          body.high-contrast-mode input,
          body.high-contrast-mode select,
          body.high-contrast-mode textarea {
            background-color: #000 !important;
            color: #fff !important;
            border: 2px solid #fff !important;
          }
          
          body.cursor-color-white * {
            cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16"><path fill="%23fff" stroke="%23000" stroke-width="0.5" d="M4.5 2.5a.5.5 0 0 1 0 1H3.706c-.351 0-.694.106-.984.3L1.5 4.5V7c0 .293.103.577.3.8l5.6 5.6a.5.5 0 0 0 .8-.8L3.4 7.8a.5.5 0 0 1-.3-.8V4.706c0-.351.106-.694.3-.984l.7-.7A.5.5 0 0 1 4.5 2.5z"/><path fill="%23fff" stroke="%23000" stroke-width="0.5" d="M7 1.5a.5.5 0 0 1 .5.5v1.05a2.5 2.5 0 0 1 0 4.9v1.05a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5z"/></svg>') 16 0, auto;
          }
          
          body.cursor-color-black * {
            cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16"><path fill="%23000" d="M4.5 2.5a.5.5 0 0 1 0 1H3.706c-.351 0-.694.106-.984.3L1.5 4.5V7c0 .293.103.577.3.8l5.6 5.6a.5.5 0 0 0 .8-.8L3.4 7.8a.5.5 0 0 1-.3-.8V4.706c0-.351.106-.694.3-.984l.7-.7A.5.5 0 0 1 4.5 2.5z"/><path fill="%23000" d="M7 1.5a.5.5 0 0 1 .5.5v1.05a2.5 2.5 0 0 1 0 4.9v1.05a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5z"/></svg>') 16 0, auto;
          }
        `;
        document.head.appendChild(styleEl);
      }
    }
  }
  </script>