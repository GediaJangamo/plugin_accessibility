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
      class="fixed bottom-32 left-0 bg-[#4A90E2] hover:bg-[#357ABD] text-white py-4 px-6 rounded-r-full shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 z-50 group"
      aria-label="Opcoes de acessibilidade"
    >
      <img src="/static/core/img/accessibility_icon.png" alt="Icone de acessibilidade" class="h-8 w-8 brightness-0 invert">
      
      <div class="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2 bg-gray-800 text-white text-sm rounded whitespace-nowrap invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-opacity duration-300 z-50">
        <div class="absolute top-1/2 right-full -mt-1 border-solid border-8 border-transparent border-r-gray-800"></div>
        Clique para opcoes de acessibilidade
      </div>
    </button>

    <!-- Accessibility menu - responsivo -->
    <div 
      v-if="isOpen" 
      class="fixed bottom-0 left-0 top-0 bg-white dark:bg-gray-900 rounded-r-lg shadow-xl border-r border-gray-200 dark:border-gray-700 z-40 transition-all duration-300 flex flex-col w-full sm:w-96 max-w-sm"
      role="dialog"
      aria-labelledby="accessibility-title"
    >
      <!-- Header with logos - mais espaçamento no topo -->
      <div class="flex items-center justify-between p-2 pt-4 bg-[#f8fafc] border-b border-gray-200 dark:border-gray-700 dark:bg-gray-900">
      
          <div class="flex justify-center items-center gap-3">
                <div class="w-10 h-10 bg-[#3b82f6] rounded-md flex items-center justify-center text-white ">G</div>
                <div class="text-[#1a202c]">
                    <h3 class="text-lg font-semibold">AccessJay</h3>
                    <p class="text-sm text-[#64758b]">Personalize sua experiência de navegação</p>
                </div>
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
      
      
      <!-- Main content - responsivo com scroll se necessário -->
      <div class="px-4 sm:px-6 py-4 space-y-2 flex-grow flex flex-col justify-between overflow-y-auto">
        <div class="space-y-4 sm:space-y-3">
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
        
        <!-- Bottom buttons - responsivo -->
        <div class="py-4 pb-6 sm:pb-4 space-y-2 sm:space-y-1">
          <!-- Save Preferences Button -->
          <button 
            @click="saveSettings" 
            class="w-full bg-[#3b82f6] hover:bg-[#357ABD] text-white py-3 sm:py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 flex items-center justify-center text-lg sm:text-base"
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
            class="w-full bg-[#f1f5f9] hover:bg-slate-50 border-[#cedff6] border-[1px] dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-800 dark:text-white py-3 sm:py-2 px-4 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center justify-center text-lg sm:text-base"
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
    
    <!-- Componentes de acessibilidade invisíveis para manter funcionalidades ativas quando o menu está fechado -->
    <div class="hidden">
      <FontSizeToggle 
        v-if="!isOpen"
        :fontSize="settings.fontSize" 
        @update:fontSize="updateSetting('fontSize', $event)"
        @announce="announceToScreenReader" 
      />
      
      <ContrastToggle 
        v-if="!isOpen"
        :highContrast="settings.highContrast" 
        @update:highContrast="updateSetting('highContrast', $event)"
        @announce="announceToScreenReader" 
      />
      
      <ScreenReader 
        v-if="!isOpen"
        :screenReader="settings.screenReader" 
        @update:screenReader="updateSetting('screenReader', $event)"
        @announce="announceToScreenReader" 
      />
      
      <VoiceNavigation 
        v-if="!isOpen"
        :voiceCommands="settings.voiceCommands" 
        @update:voiceCommands="updateSetting('voiceCommands', $event)"
        @announce="announceToScreenReader"
        @executeCommand="handleVoiceCommand" 
      />
    </div>
    
    <!-- Persistent storage for the settings across page changes -->
    <!-- <script v-if="settingsChanged" type="application/json" id="accessibility-settings-persist">
      {{ JSON.stringify(settings) }}
    </script> -->
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
      },
      settingsChanged: false,
      // Adicionar um intervalo para verificar e aplicar configurações periodicamente
      settingsInterval: null
    }
  },
  mounted() {
    this.loadSettings();
    window.addEventListener('keydown', this.handleKeyDown);
    
    // Adiciona um event listener para persistir as configurações entre navegações de página
    window.addEventListener('beforeunload', this.persistSettings);
    
    // Add global style for screen-reader-only elements
    this.addGlobalStyles();
    
    // Verifica se há configurações persistentes entre navegações
    this.checkForPersistentSettings();
    
    // Aplicar configurações imediatamente após montagem
    this.applySettings();
    
    // Configurar um intervalo para verificar e aplicar configurações periodicamente
    // Isso garante que as configurações permaneçam ativas mesmo quando o menu estiver fechado
    this.settingsInterval = setInterval(() => {
      this.applySettings();
    }, 2000); // Verificar a cada 2 segundos
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('beforeunload', this.persistSettings);

    // Limpar o intervalo quando o componente for desmontado
    if (this.settingsInterval) {
      clearInterval(this.settingsInterval);
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
      
      // Garantir que as configurações sejam aplicadas imediatamente após fechar o menu
      if (!this.isOpen) {
        this.$nextTick(() => {
          this.applySettings();
        });
      }
    },
    
    updateSetting(key, value) {
      this.settings[key] = value;
      this.settingsChanged = true;
      this.saveSettings();
      
      // Aplicar configurações imediatamente
      this.applySettings();
    },
    
    resetSettings() {
      this.settings = {
        fontSize: 'Normal',
        highContrast: false,
        screenReader: false,
        voiceCommands: false,
        cursorColor: 'black'
      };
      
      this.settingsChanged = true;
      this.saveSettings();
      this.applySettings();
      this.announceToScreenReader('Configurações restauradas para o padrão');
    },
    
    saveSettings() {
      localStorage.setItem('accessibility_settings', JSON.stringify(this.settings));
      this.settingsChanged = true;
      this.announceToScreenReader('Preferências de acessibilidade salvas');
      
      // Garantir que as configurações sejam aplicadas após salvar
      this.applySettings();
    },
    
    loadSettings() {
      const savedSettings = localStorage.getItem('accessibility_settings');
      if (savedSettings) {
        try {
          const parsedSettings = JSON.parse(savedSettings);
          this.settings = { ...this.settings, ...parsedSettings };
          // Aplicar configurações imediatamente após carregar
          this.applySettings();
        } catch (e) {
          console.error('Erro ao carregar configurações:', e);
        }
      }
    },
    
    persistSettings() {
      // Salva as configurações em um script de dados para recuperação após navegação
      const scriptElement = document.getElementById('accessibility-settings-persist');
      if (scriptElement) {
        scriptElement.textContent = JSON.stringify(this.settings);
      }
    },
    
    checkForPersistentSettings() {
      // Procura por configurações persistentes em recarregamentos/navegações
      const persistedElement = document.getElementById('accessibility-settings-persist');
      if (persistedElement) {
        try {
          const persistedSettings = JSON.parse(persistedElement.textContent);
          this.settings = { ...this.settings, ...persistedSettings };
          this.applySettings();
        } catch (e) {
          console.error('Erro ao recuperar configurações persistentes:', e);
        }
      }
    },
    
    applySettings() {
      // Aplicar configurações de tamanho de fonte
      const fontSize = {
        'Pequeno': '0.85rem',
        'Normal': '1rem',
        'Grande': '1.15rem',
        'Muito Grande': '1.3rem'
      }[this.settings.fontSize] || '1rem';
      
      // Aplicar ao documento inteiro, não apenas ao main-content
      // document.documentElement.style.fontSize = fontSize;
  
      // Aplicar fontsize ao main-content
      const mainContent = document.getElementById('main-content');
      if (mainContent) {
        mainContent.style.fontSize = fontSize;
      }
      
      // Aplicar configurações de alto contraste
      if (this.settings.highContrast) {
        document.body.classList.add('high-contrast');
      } else {
        document.body.classList.remove('high-contrast');
      }
      
      // Configurações de cursor personalizado
      document.body.style.cursor = this.settings.cursorColor === 'white' ? 
        'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'24\' height=\'24\' viewBox=\'0 0 24 24\' fill=\'white\'%3E%3Cpath d=\'M13 21l-7-7h14l-7 7z\'/%3E%3C/svg%3E"), auto' :
        'default';
        
      // Garantir que as configurações de leitor de tela e comandos de voz permaneçam ativas
      if (this.settings.screenReader) {
        // Lógica para manter o leitor de tela ativo
        this.ensureScreenReaderActive();
      }
      
      if (this.settings.voiceCommands) {
        // Lógica para manter os comandos de voz ativos
        this.ensureVoiceCommandsActive();
      }
    },
    
    ensureScreenReaderActive() {
      // Esta função garante que o leitor de tela permaneça ativo
      // Implementação depende do componente ScreenReader
      // Aqui você pode adicionar lógica específica para manter o leitor ativo
      const screenReaderEvent = new CustomEvent('ensure-screen-reader-active', {
        detail: { active: true }
      });
      document.dispatchEvent(screenReaderEvent);
    },
    
    ensureVoiceCommandsActive() {
      // Esta função garante que os comandos de voz permaneçam ativos
      // Implementação depende do componente VoiceNavigation
      // Aqui você pode adicionar lógica específica para manter os comandos de voz ativos
      const voiceCommandsEvent = new CustomEvent('ensure-voice-commands-active', {
        detail: { active: true }
      });
      document.dispatchEvent(voiceCommandsEvent);
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
      // Atalho Alt+A para abrir/fechar o menu de acessibilidade
      if (event.altKey && event.key === 'a') {
        this.toggleMenu();
        event.preventDefault();
      }
      
      // Atalho Ctrl+Alt+H para alternar alto contraste
      if (event.ctrlKey && event.altKey && event.key === 'h') {
        this.updateSetting('highContrast', !this.settings.highContrast);
        event.preventDefault();
      }
      
      // Atalho Ctrl+Alt+S para alternar leitor de tela
      if (event.ctrlKey && event.altKey && event.key === 's') {
        this.updateSetting('screenReader', !this.settings.screenReader);
        event.preventDefault();
      }
      
      // Atalho Ctrl+Alt+V para alternar comandos de voz
      if (event.ctrlKey && event.altKey && event.key === 'v') {
        this.updateSetting('voiceCommands', !this.settings.voiceCommands);
        event.preventDefault();
      }
      
      // Atalhos para tamanho de fonte
      if (event.ctrlKey && event.altKey) {
        if (event.key === '1') {
          this.updateSetting('fontSize', 'Pequeno');
          event.preventDefault();
        } else if (event.key === '2') {
          this.updateSetting('fontSize', 'Normal');
          event.preventDefault();
        } else if (event.key === '3') {
          this.updateSetting('fontSize', 'Grande');
          event.preventDefault();
        } else if (event.key === '4') {
          this.updateSetting('fontSize', 'Muito Grande');
          event.preventDefault();
        }
      }
    },
    
    addGlobalStyles() {
      // Adiciona estilos globais para acessibilidade
      const styleEl = document.createElement('style');
      styleEl.id = 'accessibility-global-styles';
      styleEl.innerHTML = `
        /* Classes para Alto Contraste */
        body.high-contrast {
          background-color: #000 !important;
          color: #fff !important;
        }
        
        body.high-contrast a {
          color: #00ccff !important;
          text-decoration: underline !important;
        }
        
        body.high-contrast button, 
        body.high-contrast input, 
        body.high-contrast select, 
        body.high-contrast textarea {
          background-color: #000 !important;
          color: #fff !important;
          border: 2px solid #fff !important;
        }
        
        body.high-contrast img {
          filter: grayscale(100%) contrast(150%) !important;
        }
        
        /* Classe para elementos visíveis apenas para leitores de tela */
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
      `;
      document.head.appendChild(styleEl);
    },
    
    handleVoiceCommand(command) {
      // Processar comandos de voz
      const commands = {
        "abrir menu": () => {
          if (!this.isOpen) this.toggleMenu();
        },
        "fechar menu": () => {
          if (this.isOpen) this.toggleMenu();
        },
        "ativar alto contraste": () => {
          if (!this.settings.highContrast) this.updateSetting('highContrast', true);
        },
        "desativar alto contraste": () => {
          if (this.settings.highContrast) this.updateSetting('highContrast', false);
        },
        "ativar leitor": () => {
          if (!this.settings.screenReader) this.updateSetting('screenReader', true);
        },
        "desativar leitor": () => {
          if (this.settings.screenReader) this.updateSetting('screenReader', false);
        },
        "aumentar fonte": () => {
          const sizes = ['Pequeno', 'Normal', 'Grande', 'Muito Grande'];
          const currentIndex = sizes.indexOf(this.settings.fontSize);
          if (currentIndex < sizes.length - 1) {
            this.updateSetting('fontSize', sizes[currentIndex + 1]);
          }
        },
        "diminuir fonte": () => {
          const sizes = ['Pequeno', 'Normal', 'Grande', 'Muito Grande'];
          const currentIndex = sizes.indexOf(this.settings.fontSize);
          if (currentIndex > 0) {
            this.updateSetting('fontSize', sizes[currentIndex - 1]);
          }
        },
        "salvar configurações": () => {
          this.saveSettings();
        },
        "restaurar padrão": () => {
          this.resetSettings();
        }
      };
      
      // Execute o comando se existir
      const commandFn = commands[command.toLowerCase()];
      if (commandFn) {
        commandFn();
        this.announceToScreenReader(`Comando executado: ${command}`);
      } else {
        this.announceToScreenReader(`Comando não reconhecido: ${command}`);
      }
    }
  }
}
</script>

<style>
/* Estilos específicos do componente */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

/* Animações para o menu de acessibilidade */
.fixed[role="dialog"] {
  animation: slideIn 0.3s ease-out, fadeIn 0.3s ease-out;
}

/* Melhorias responsivas */
@media (max-width: 640px) {
  .fixed[role="dialog"] {
    width: 100% !important;
    max-width: none !important;
  }
}
</style>