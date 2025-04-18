<template>
  <div>
    <!-- Skip link for accessibility -->
    <a href="#main-content" class="absolute -left-[9999px] top-auto w-px h-px overflow-hidden focus:fixed focus:top-0 focus:left-0 focus:w-auto focus:h-auto focus:p-2 focus:bg-white focus:text-black focus:font-bold focus:z-50 focus:shadow-lg focus:no-underline">
      Pular para o conteúdo principal
    </a>

    <!-- Accessibility button - only visible when menu is closed -->
    <button 
      v-if="!isOpen"
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

    <!-- Accessibility menu - wider and full-height, with better spacing -->
    <div 
      v-if="isOpen" 
      class="fixed bottom-0 left-0 top-0 bg-white dark:bg-gray-900 rounded-r-lg shadow-xl border-r border-gray-200 dark:border-gray-700 z-40 transition-all duration-300 flex flex-col w-96"
      role="dialog"
      aria-labelledby="accessibility-title"
    >
      <!-- Header with logos -->
      <div class="flex items-center justify-between p-2 bg-white border-b border-gray-200 dark:border-gray-700 dark:bg-gray-900">
        <div class="flex items-center space-x-3">
          <img src="/static/core/img/logo-uem.png" alt="Logo UEM" class="h-16">
          <div class="border-l border-gray-300 dark:border-gray-600 h-12"></div>
          <img src="/static/core/img/siga.png" alt="Logo SIGA" class="h-8">
        </div>
        
        <button 
          @click="toggleMenu" 
          class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 p-1 rounded-full"
          aria-label="Fechar menu de acessibilidade"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="p-2 bg-[#077b4b] mb-2">
        <h2 id="accessibility-title" class="text-2xl font-poppins text-white dark:text-white flex items-center justify-center">
          Acessibilidade
        </h2>
      </div>
      
      <!-- Main content with reduced spacing between items -->
      <div class="px-4 space-y-2 flex-grow flex flex-col justify-between">
        <div class="space-y-3">
          <!-- Font size control component -->
          <FontSizeToggle 
            :fontSize="settings.fontSize" 
            @update:fontSize="updateSetting('fontSize', $event)"
            @announce="announceToScreenReader" 
          />
          
          <!-- High contrast component -->
          <ContrastToggle 
            :highContrast="settings.highContrast" 
            @update:highContrast="updateSetting('highContrast', $event)"
            @announce="announceToScreenReader" 
          />
          
          <!-- Screen reader component -->
          <ScreenReader 
            :screenReader="settings.screenReader" 
            @update:screenReader="updateSetting('screenReader', $event)"
            @announce="announceToScreenReader" 
          />
          
          <!-- Voice commands component -->
          <VoiceNavigation 
            :voiceCommands="settings.voiceCommands" 
            @update:voiceCommands="updateSetting('voiceCommands', $event)"
            @announce="announceToScreenReader"
            @executeCommand="handleVoiceCommand" 
          />
          
          <!-- Cursor section component -->
          <CursorCustomizer 
            :cursorColor="settings.cursorColor" 
            @update:cursorColor="updateSetting('cursorColor', $event)"
          />
        </div>
        
        <!-- Bottom buttons -->
        <div class="py-2 mb-4 space-y-1">
          <!-- Save Preferences Button -->
          <button 
            @click="saveSettings" 
            class="w-full bg-[#077b4b] hover:bg-green-600 text-white py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 flex items-center justify-center text-lg"
            aria-label="Salvar preferências de acessibilidade"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            Salvar Preferências
          </button>
          
          <!-- Reset Settings Button -->
          <button 
            @click="resetSettings" 
            class="w-full bg-gray-200 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-800 dark:text-white py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center justify-center text-lg"
            aria-label="Restaurar configurações padrão"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Restaurar Configurações Padrão
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FontSizeToggle from './options/FontSizeToggle.vue';
import ContrastToggle from './options/ContrastToggle.vue';
import ScreenReader from './options/ScreenReader.vue';
import VoiceNavigation from './options/VoiceNavigation.vue';
import CursorCustomizer from './options/CursorCustomizer.vue';

export default {
  name: 'AccessibilityComponent',
  components: {
    FontSizeToggle,
    ContrastToggle,
    ScreenReader,
    VoiceNavigation,
    CursorCustomizer
  },
  data() {
    return {
      isOpen: false,
      settings: {
        fontSize: 'Normal',
        highContrast: false,
        screenReader: false,
        voiceCommands: false,
        cursorColor: 'black'
      }
    }
  },
  mounted() {
    this.loadSettings();
    window.addEventListener('keydown', this.handleKeyDown);
    
    // Add global style for screen-reader-only elements
    this.addGlobalStyles();
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
    
    updateSetting(key, value) {
      this.settings[key] = value;
      this.saveSettings();
    },
    
    resetSettings() {
      this.settings = {
        fontSize: 'Normal',
        highContrast: false,
        screenReader: false,
        voiceCommands: false,
        cursorColor: 'black'
      };
      
      this.saveSettings();
      this.announceToScreenReader('Configurações restauradas para o padrão');
    },
    
    saveSettings() {
      localStorage.setItem('accessibility_settings', JSON.stringify(this.settings));
    },
    
    loadSettings() {
      const savedSettings = localStorage.getItem('accessibility_settings');
      if (savedSettings) {
        this.settings = { ...this.settings, ...JSON.parse(savedSettings) };
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
    
    handleVoiceCommand(command) {
      if (command.includes('aumentar fonte') || command.includes('aumentar tamanho')) {
        this.updateSetting('fontSize', 'Grande');
      } else if (command.includes('diminuir fonte') || command.includes('diminuir tamanho')) {
        this.updateSetting('fontSize', 'Pequeno');
      } else if (command.includes('alto contraste')) {
        this.updateSetting('highContrast', !this.settings.highContrast);
      } else if (command.includes('resetar') || command.includes('restaurar')) {
        this.resetSettings();
      } else if (command.includes('fechar menu')) {
        this.isOpen = false;
      } else if (command.includes('cursor branco')) {
        this.updateSetting('cursorColor', 'white');
      } else if (command.includes('cursor preto')) {
        this.updateSetting('cursorColor', 'black');
      }
    },
    
    // No final do método addGlobalStyles() do componente principal
// No componente principal, modifique o método addGlobalStyles
addGlobalStyles() {
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
    
    /* Isolar o menu de acessibilidade das mudanças de fonte */
    [role="dialog"] {
      font-size: 16px !important;
    }
    
    /* Estilo para o código de exclusão do menu do seletor de fonte */
    [role="dialog"] * {
      font-size: inherit !important;
    }
    
    /* Certifique-se de que o corpo da página possa ser alvo das mudanças de fonte */
    body {
      transition: font-size 0.3s ease;
    }
  `;
  document.head.appendChild(styleEl);
  
  // Adicione uma classe ao corpo para identificar o conteúdo principal
  if (!document.getElementById('main-content')) {
    // Se não houver um elemento main-content, adicione uma div para conter o conteúdo principal
    const mainContent = document.createElement('div');
    mainContent.id = 'main-content';
    
    // Mova todo o conteúdo do body (exceto o menu de acessibilidade) para esta div
    const accessibilityMenu = document.querySelector('[role="dialog"]');
    const bodyChildren = Array.from(document.body.children);
    
    bodyChildren.forEach(child => {
      if (child !== accessibilityMenu && child !== styleEl) {
        mainContent.appendChild(child);
      }
    });
    
    document.body.appendChild(mainContent);
  }
}

    
  }
}
</script>