<!-- Leitor de tela -->
<template>
    <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Leitor de Tela</span>
          <span class="text-sm text-gray-600 dark:text-gray-300">Narração de conteúdos</span>
        </div>
        <div class="flex items-center">
          <input 
            type="checkbox" 
            id="screen-reader" 
            :checked="screenReader" 
            @change="toggleScreenReader" 
            class="sr-only"
          >
          <div class="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': screenReader}">
            <div class="absolute left-1 top-1 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-7': screenReader}"></div>
          </div>
        </div>
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ScreenReader',
    props: {
      screenReader: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      toggleScreenReader() {
        const newValue = !this.screenReader;
        this.$emit('update:screenReader', newValue);
        this.$emit('announce', newValue ? 'Leitor de tela ativado' : 'Leitor de tela desativado');
      }
      // Funções adicionais específicas do leitor de tela podem ser implementadas aqui
    }
  }
  </script>