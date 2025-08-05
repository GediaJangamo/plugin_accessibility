<!-- Alto contraste -->
<template>
    <div class="p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
         
          <svg xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="h-7 w-7 text-[#3b82f6]">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 18a6 6 0 0 0 0-12v12z" />
        </svg>

        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Alto Contraste</span>
          <span class="text-sm text-[#64748b] dark:text-gray-300">Melhora visualização de textos</span>
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
          body.high-contrast-mode switch,
          body.high-contrast-mode toggle,
          body.high-contrast-mode input,
          body.high-contrast-mode select,
          body.high-contrast-mode textarea {
            background-color: #000 !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
          }
        `;
        document.head.appendChild(styleEl);
      }
    }
  }
  </script>