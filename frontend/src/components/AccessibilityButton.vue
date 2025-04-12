<template>
  <button @click="toggleMenu" 
          class="fixed bottom-4 right-4 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 accessibility-button z-50"
          aria-label="Opções de acessibilidade">
    <!-- SVG do ícone de cadeira de rodas (acessibilidade) -->
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <circle cx="12" cy="6" r="3" stroke-width="2"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 21v-4m0 0H7c-.55 0-1-.45-1-1v-4m0 0h12M6 12V8c0-.55.45-1 1-1h4"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 17h-4.09c-.86 0-1.66-.53-1.98-1.35L8 12"/>
    </svg>
  </button>
</template>
  
  <script>
  export default {
    name: 'AccessibilityButton',
    methods: {
      toggleMenu() {
        this.$emit('toggle-menu')
      }
    }
  }
  </script>