<template>
    <transition name="slide-fade">
      <div 
        v-if="isOpen" 
        class="fixed bottom-32 left-0 bg-white dark:bg-gray-900 rounded-lg shadow-xl p-5 w-80 border border-gray-200 dark:border-gray-700 z-40"
        role="dialog"
        aria-labelledby="accessibility-title"
      >
        <!-- Cabeçalho com logos -->
        <div class="flex items-center justify-between mb-4 border-b pb-3 border-gray-200 dark:border-gray-700">
          <div class="flex items-center space-x-3">
            <img src="/static/core/img/uem_logo.png" alt="Logo UEM" class="h-8">
            <div class="border-l border-gray-300 dark:border-gray-600 h-8"></div>
            <img src="/static/core/img/siga_logo.png" alt="Logo SIGA" class="h-6">
          </div>
          
          <button 
            @click="$emit('close-menu')" 
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 p-1 rounded-full"
            aria-label="Fechar menu de acessibilidade"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <h2 id="accessibility-title" class="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-[#246647]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Acessibilidade SIGA
        </h2>
        
        <div class="space-y-5">
          <!-- Controle de tamanho da fonte -->
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
          
          <!-- Controle de alto contraste -->
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
          
          <!-- Leitor de tela -->
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
          
          <!-- Comandos por voz -->
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
    </transition>
  </template>
  
  <script>
  export default {
    name: 'AccessibilityMenu',
    props: {
      isOpen: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        fontSize: 'Normal',
        highContrast: false,
        screenReader: false,
        voiceCommands: false
      }
    },
    methods: {
      increaseFont() {
        const body = document.body
        const currentSize = window.getComputedStyle(body).fontSize
        const newSize = parseFloat(currentSize) * 1.1
        body.style.fontSize = `${newSize}px`
        this.fontSize = 'Grande'
        this.saveSettings()
        
        // Feedback para usuários de leitores de tela
        this.announceToScreenReader('Tamanho da fonte aumentado')
      },
      
      decreaseFont() {
        const body = document.body
        const currentSize = window.getComputedStyle(body).fontSize
        const newSize = parseFloat(currentSize) * 0.9
        body.style.fontSize = `${newSize}px`
        this.fontSize = 'Pequeno'
        this.saveSettings()
        
        // Feedback para usuários de leitores de tela
        this.announceToScreenReader('Tamanho da fonte diminuído')
      },
      
      toggleContrast() {
        if (this.highContrast) {
          document.body.classList.add('high-contrast')
          document.documentElement.style.setProperty('--bg-color', '#000')
          document.documentElement.style.setProperty('--text-color', '#fff')
          
          // Classe para alto contraste
          document.body.classList.add('high-contrast-mode')
          
          // Feedback para usuários de leitores de tela
          this.announceToScreenReader('Alto contraste ativado')
        } else {
          document.body.classList.remove('high-contrast')
          document.documentElement.style.removeProperty('--bg-color')
          document.documentElement.style.removeProperty('--text-color')
          
          // Remover classe de alto contraste
          document.body.classList.remove('high-contrast-mode')
          
          // Feedback para usuários de leitores de tela
          this.announceToScreenReader('Alto contraste desativado')
        }
        this.saveSettings()
      },
      
      toggleScreenReader() {
        // Feedback visual e sonoro para usuários
        this.announceToScreenReader(
          this.screenReader ? 'Leitor de tela ativado' : 'Leitor de tela desativado'
        )
        this.saveSettings()
      },
      
      toggleVoiceCommands() {
        // Feedback visual e sonoro para usuários
        this.announceToScreenReader(
          this.voiceCommands ? 'Comandos por voz ativados' : 'Comandos por voz desativados'
        )
        this.saveSettings()
      },
      
      resetSettings() {
        // Restaurar tamanho de fonte
        document.body.style.fontSize = ''
        this.fontSize = 'Normal'
        
        // Restaurar contraste
        this.highContrast = false
        document.body.classList.remove('high-contrast')
        document.body.classList.remove('high-contrast-mode')
        document.documentElement.style.removeProperty('--bg-color')
        document.documentElement.style.removeProperty('--text-color')
        
        // Desativar leitor de tela
        this.screenReader = false
        
        // Desativar comandos por voz
        this.voiceCommands = false
        
        this.saveSettings()
        
        // Feedback para usuários de leitores de tela
        this.announceToScreenReader('Configurações restauradas para o padrão')
      },
      
      saveSettings() {
        // Salvar configurações através do localStorage
        const settings = {
          fontSize: this.fontSize,
          highContrast: this.highContrast,
          screenReader: this.screenReader,
          voiceCommands: this.voiceCommands
        }
        
        localStorage.setItem('accessibility_settings', JSON.stringify(settings))
        
        // Aqui você poderia também salvar via API para o seu backend Django
      },
      
      loadSettings() {
        // Carregar configurações do localStorage
        const savedSettings = localStorage.getItem('accessibility_settings')
        if (savedSettings) {
          const settings = JSON.parse(savedSettings)
          this.fontSize = settings.fontSize || 'Normal'
          this.highContrast = settings.highContrast || false
          this.screenReader = settings.screenReader || false
          this.voiceCommands = settings.voiceCommands || false
          
          // Aplicar configurações
          if (this.highContrast) {
            this.toggleContrast()
          }
          
          // Aplicar tamanho da fonte
          if (this.fontSize !== 'Normal') {
            const factor = this.fontSize === 'Grande' ? 1.1 : 0.9
            const body = document.body
            const defaultSize = '16px' // tamanho padrão na maioria dos navegadores
            const currentSize = parseFloat(defaultSize)
            body.style.fontSize = `${currentSize * factor}px`
          }
        }
      },
      
      // Função auxiliar para anunciar mudanças para leitores de tela
      announceToScreenReader(message) {
        // Criar um elemento live region para leitores de tela
        const announcement = document.createElement('div')
        announcement.setAttribute('aria-live', 'assertive')
        announcement.setAttribute('class', 'sr-only')
        announcement.textContent = message
        
        document.body.appendChild(announcement)
        
        // Remover após a leitura (normalmente 3 segundos é suficiente)
        setTimeout(() => {
          document.body.removeChild(announcement)
        }, 3000)
      }
    },
    mounted() {
      this.loadSettings()
    }
  }
  </script>
  
  <style scoped>
  /* Transição para o menu */
  .slide-fade-enter-active {
    transition: all 0.3s ease-out;
  }
  
  .slide-fade-leave-active {
    transition: all 0.3s ease-in;
  }
  
  .slide-fade-enter-from,
  .slide-fade-leave-to {
    transform: translateX(-30px);
    opacity: 0;
  }
  
  /* Estilo global para alto contraste */
  :global(.high-contrast-mode) {
    --bg-color: #000000;
    --text-color: #ffffff;
    --link-color: #ffff00;
    --border-color: #ffffff;
  }
  
  :global(.high-contrast-mode *) {
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
    border-color: var(--border-color) !important;
  }
  
  :global(.high-contrast-mode a) {
    color: var(--link-color) !important;
    text-decoration: underline !important;
  }
  
  :global(.high-contrast-mode img) {
    filter: grayscale(100%) !important;
  }
  
  :global(.high-contrast-mode button) {
    border: 2px solid var(--border-color) !important;
  }
  </style>