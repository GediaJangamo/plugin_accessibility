<template>
  <div v-if="isOpen" class="fixed bottom-32 left-20 bg-white rounded-lg shadow-xl p-4 w-64 border border-gray-200 z-40">
      <h2 class="text-lg font-bold mb-3 text-gray-800">Acessibilidade</h2>
      
      <div class="space-y-4">
        <!-- Controle de tamanho da fonte -->
        <div>
          <h3 class="font-medium text-gray-700 mb-2">Tamanho da Fonte</h3>
          <div class="flex items-center justify-between">
            <button @click="decreaseFont" 
                    class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1 rounded"
                    aria-label="Diminuir fonte">A-</button>
            <span class="text-gray-600">{{ fontSize }}</span>
            <button @click="increaseFont" 
                    class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1 rounded"
                    aria-label="Aumentar fonte">A+</button>
          </div>
        </div>
        
        <!-- Controle de alto contraste -->
        <div>
          <label class="flex items-center cursor-pointer">
            <input type="checkbox" v-model="highContrast" @change="toggleContrast" class="form-checkbox h-5 w-5 text-blue-600">
            <span class="ml-2 text-gray-700">Alto Contraste</span>
          </label>
        </div>
        
        <!-- Leitor de tela -->
        <div>
          <label class="flex items-center cursor-pointer">
            <input type="checkbox" v-model="screenReader" @change="toggleScreenReader" class="form-checkbox h-5 w-5 text-blue-600">
            <span class="ml-2 text-gray-700">Leitor de Tela</span>
          </label>
        </div>
        
        <!-- Comandos por voz -->
        <div>
          <label class="flex items-center cursor-pointer">
            <input type="checkbox" v-model="voiceCommands" @change="toggleVoiceCommands" class="form-checkbox h-5 w-5 text-blue-600">
            <span class="ml-2 text-gray-700">Comandos por Voz</span>
          </label>
        </div>
      </div>
      
      <div class="mt-4 pt-3 border-t border-gray-200">
        <button @click="resetSettings" 
                class="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 px-4 rounded"
                aria-label="Restaurar configurações padrão">
          Restaurar Padrão
        </button>
      </div>
    </div>

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
      },
      decreaseFont() {
        const body = document.body
        const currentSize = window.getComputedStyle(body).fontSize
        const newSize = parseFloat(currentSize) * 0.9
        body.style.fontSize = `${newSize}px`
        this.fontSize = 'Pequeno'
        this.saveSettings()
      },
      toggleContrast() {
        if (this.highContrast) {
          document.body.classList.add('high-contrast')
          document.documentElement.style.setProperty('--bg-color', '#000')
          document.documentElement.style.setProperty('--text-color', '#fff')
        } else {
          document.body.classList.remove('high-contrast')
          document.documentElement.style.removeProperty('--bg-color')
          document.documentElement.style.removeProperty('--text-color')
        }
        this.saveSettings()
      },
      toggleScreenReader() {
        // A implementação real exigiria integração com APIs de leitor de tela
        console.log('Leitor de Tela:', this.screenReader ? 'Ativado' : 'Desativado')
        this.saveSettings()
      },
      toggleVoiceCommands() {
        // A implementação real exigiria integração com APIs de reconhecimento de voz
        console.log('Comandos por Voz:', this.voiceCommands ? 'Ativados' : 'Desativados')
        this.saveSettings()
      },
      resetSettings() {
        // Restaurar tamanho de fonte
        document.body.style.fontSize = ''
        this.fontSize = 'Normal'
        
        // Restaurar contraste
        this.highContrast = false
        document.body.classList.remove('high-contrast')
        document.documentElement.style.removeProperty('--bg-color')
        document.documentElement.style.removeProperty('--text-color')
        
        // Desativar leitor de tela
        this.screenReader = false
        
        // Desativar comandos por voz
        this.voiceCommands = false
        
        this.saveSettings()
      },
      saveSettings() {
        // Salvar configurações através da API ou localStorage
        const settings = {
          fontSize: this.fontSize,
          highContrast: this.highContrast,
          screenReader: this.screenReader,
          voiceCommands: this.voiceCommands
        }
        
        // Opção 1: Salvar no localStorage
        localStorage.setItem('accessibility_settings', JSON.stringify(settings))
        
        // Opção 2: Enviar para API do Django
        fetch('/api/accessibility/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(settings),
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error))
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
      }
    },
    mounted() {
      this.loadSettings()
    }
  }
  </script>