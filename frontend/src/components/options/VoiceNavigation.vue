<template>
  <div class="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-lg border border-blue-200 dark:border-gray-600 hover:shadow-lg transition-all duration-300">
    <label class="flex items-center cursor-pointer group">
      <div class="flex-shrink-0 mr-4">
        <div class="relative">
          <!-- Ícone principal -->
          <svg xmlns="http://www.w3.org/2000/svg" 
               viewBox="0 0 24 24" 
               fill="none" 
               stroke="currentColor" 
               stroke-width="1.8" 
               stroke-linecap="round" 
               stroke-linejoin="round" 
               class="h-8 w-8 text-blue-600 dark:text-blue-400 group-hover:text-blue-700 dark:group-hover:text-blue-300 transition-colors">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
          
          <!-- Indicador de status -->
          <div v-if="voiceCommands" 
               class="absolute -top-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white dark:border-gray-800 rounded-full animate-pulse">
          </div>
        </div>
      </div>
      
      <div class="flex-grow">
        <span class="block text-lg font-semibold text-gray-800 dark:text-white group-hover:text-blue-700 dark:group-hover:text-blue-300 transition-colors">
          Comandos de Voz
        </span>
        <span class="text-sm text-gray-600 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-colors">
          {{ voiceCommands ? 'Sistema ativo - Navegue com sua voz' : 'Ativar navegação por comandos de voz' }}
        </span>
        
        <!-- Dicas de uso quando ativo -->
        <div v-if="voiceCommands" class="mt-2 text-xs text-blue-600 dark:text-blue-400">
          <div class="flex items-center space-x-4">
            <span class="flex items-center">
              <kbd class="px-1 py-0.5 bg-blue-100 dark:bg-blue-900 rounded text-xs">Ctrl+M</kbd>
              <span class="ml-1">Microfone</span>
            </span>
            <span class="flex items-center">
              <kbd class="px-1 py-0.5 bg-blue-100 dark:bg-blue-900 rounded text-xs">Ctrl+H</kbd>
              <span class="ml-1">Ajuda</span>
            </span>
            <span class="flex items-center">
              <kbd class="px-1 py-0.5 bg-blue-100 dark:bg-blue-900 rounded text-xs">Esc</kbd>
              <span class="ml-1">Fechar</span>
            </span>
          </div>
        </div>
      </div>
      
      <div class="flex items-center ml-4">
        <input
          type="checkbox"
          id="voice-commands"
          :checked="voiceCommands"
          @change="toggleVoiceCommands"
          class="sr-only"
        >
        <div 
          class="relative w-16 h-8 bg-gray-300 dark:bg-gray-600 rounded-full transition-all duration-300 ease-in-out shadow-inner"
          :class="{'bg-gradient-to-r from-green-400 to-green-600': voiceCommands}"
        >
          <div 
            class="absolute top-1 left-1 bg-white w-6 h-6 rounded-full shadow-lg transition-all duration-300 ease-in-out flex items-center justify-center"
            :class="{'transform translate-x-8': voiceCommands}"
          >
            <!-- Ícone no toggle -->
            <svg v-if="voiceCommands" 
                 xmlns="http://www.w3.org/2000/svg" 
                 class="h-3 w-3 text-green-600" 
                 viewBox="0 0 20 20" 
                 fill="currentColor">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <svg v-else 
                 xmlns="http://www.w3.org/2000/svg" 
                 class="h-3 w-3 text-gray-400" 
                 viewBox="0 0 20 20" 
                 fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
      </div>
    </label>

    <!-- Status adicional quando ativo -->
    <div v-if="voiceCommands" class="mt-4 pt-3 border-t border-blue-200 dark:border-gray-600">
      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center space-x-4">
          <div class="flex items-center text-green-600 dark:text-green-400">
            <div class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            <span class="font-medium">Sistema Ativo</span>
          </div>
          <div class="text-gray-600 dark:text-gray-400">
            Diga <strong>"ajuda"</strong> para ver comandos
          </div>
        </div>
        <button
          @click="showQuickHelp = !showQuickHelp"
          class="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-xs hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
        >
          {{ showQuickHelp ? 'Ocultar' : 'Comandos' }}
        </button>
      </div>

      <!-- Quick help -->
      <div v-if="showQuickHelp" class="mt-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
        <div v-for="(desc, cmd) in quickCommands" :key="cmd" 
             class="bg-blue-50 dark:bg-blue-900/20 rounded px-2 py-1 text-xs">
          <div class="font-semibold text-blue-800 dark:text-blue-300">"{{ cmd }}"</div>
          <div class="text-blue-600 dark:text-blue-400">{{ desc }}</div>
        </div>
      </div>
    </div>
    
    <!-- Teleport do controlador -->
    <teleport to="body">
      <VoiceCommandController 
        :active="voiceCommands"
        @announce="announceMessage"
        @executeCommand="handleCommand"
        @update:active="handleActiveChange"
      />
    </teleport>
  </div>
</template>

<script>
import VoiceCommandController from '../controller/VoiceCommandController.vue';

export default {
  name: 'VoiceNavigation',
  components: {
    VoiceCommandController
  },
  props: {
    voiceCommands: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showQuickHelp: false,
      quickCommands: {
        "ir para início": "Página inicial",
        "abrir avaliações": "Módulo de avaliações",
        "abrir inscrições": "Módulo de inscrições",
        "abrir matrículas": "Módulo de matrículas",
        "voltar": "Página anterior",
        "onde estou": "Página atual",
        "rolar para baixo": "Rolar página",
        "aumentar fonte": "Acessibilidade",
        "ativar alto contraste": "Alto contraste"
      }
    }
  },
  methods: {
    toggleVoiceCommands() {
      const newValue = !this.voiceCommands;
      this.$emit('update:voiceCommands', newValue);
      
      // Anuncia mudança de estado
      const message = newValue ? 
        'Sistema de comandos de voz ativado' : 
        'Sistema de comandos de voz desativado';
      this.$emit('announce', message);
    },
    
    handleActiveChange(newValue) {
      // Quando o controlador se fecha, atualiza o estado
      this.$emit('update:voiceCommands', newValue);
    },
    
    announceMessage(message) {
      this.$emit('announce', message);
    },
    
    handleCommand(command) {
      this.$emit('executeCommand', command);
    }
  }
}
</script>

<style scoped>
/* Transições suaves */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Animações */
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

/* Estilo dos atalhos de teclado */
kbd {
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-weight: 600;
  box-shadow: inset 0 -2px 0 #e2e8f0, inset 0 0 1px 1px #f8fafc, 0 1px 2px 1px rgba(30,35,90,0.4);
}

.dark kbd {
  box-shadow: inset 0 -2px 0 #374151, inset 0 0 1px 1px #4b5563, 0 1px 2px 1px rgba(0,0,0,0.4);
}

/* Estados de hover aprimorados */
.group:hover .group-hover\:text-blue-700 {
  color: #1d4ed8;
}

.dark .group:hover .dark\:group-hover\:text-blue-300 {
  color: #93c5fd;
}

/* Gradientes personalizados */
.bg-gradient-to-r.from-blue-50.to-indigo-50 {
  background-image: linear-gradient(to right, #eff6ff, #eef2ff);
}

.dark .dark\:from-gray-800.dark\:to-gray-700 {
  background-image: linear-gradient(to right, #1f2937, #374151);
}

.bg-gradient-to-r.from-green-400.to-green-600 {
  background-image: linear-gradient(to right, #4ade80, #16a34a);
}
</style>