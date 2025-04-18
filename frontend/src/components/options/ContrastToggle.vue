<!-- Alto contraste -->
<template>
    <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Alto Contraste</span>
          <span class="text-sm text-gray-600 dark:text-gray-300">Melhora visualização de textos</span>
        </div>
        <div class="flex items-center">
          <input 
            type="checkbox" 
            id="high-contrast" 
            :checked="highContrast" 
            @change="toggleContrast" 
            class="sr-only"
          >
          <div class="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': highContrast}">
            <div class="absolute left-1 top-1 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-7': highContrast}"></div>
          </div>
        </div>
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ContrastToggle',
    props: {
      highContrast: {
        type: Boolean,
        default: false
      }
    },
    watch: {
      highContrast: {
        immediate: true,
        handler(newValue) {
          this.applyContrast(newValue);
        }
      }
    },
    mounted() {
      this.addContrastStyles();
    },
    methods: {
      toggleContrast() {
        this.$emit('update:highContrast', !this.highContrast);
        this.$emit('announce', !this.highContrast ? 'Alto contraste ativado' : 'Alto contraste desativado');
      },
      
      applyContrast(isHighContrast) {
        if (isHighContrast) {
          document.body.classList.add('high-contrast');
          document.documentElement.style.setProperty('--bg-color', '#000');
          document.documentElement.style.setProperty('--text-color', '#fff');
          document.body.classList.add('high-contrast-mode');
        } else {
          document.body.classList.remove('high-contrast');
          document.documentElement.style.removeProperty('--bg-color');
          document.documentElement.style.removeProperty('--text-color');
          document.body.classList.remove('high-contrast-mode');
        }
      },
      
      addContrastStyles() {
        const styleEl = document.createElement('style');
        styleEl.innerHTML = `
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
        `;
        document.head.appendChild(styleEl);
      }
    }
  }
  </script>