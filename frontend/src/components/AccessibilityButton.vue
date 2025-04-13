<script setup>


</script>

  <template>
    <div class="relative">
      <button 
        @click="toggleMenu"
        class="fixed bottom-32 left-0 bg-[#246647] hover:bg-[#579676] text-white py-4 px-6 rounded-r-full shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 z-50 group"
        aria-label="Opcoes de acessibilidade"
      >
        <img 
          src="../assets/img/accessibility_icon.png"
          alt="Icone de acessibilidade"
          class="h-8 w-8 brightness-0 invert"
        >
        
        <!-- Tooltip usando apenas Tailwind -->
        <div class="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2 bg-gray-800 text-white text-sm rounded whitespace-nowrap invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-opacity duration-300 z-50">
          <!-- Triângulo/seta do tooltip -->
          <div class="absolute top-1/2 right-full -mt-1 border-solid border-8 border-transparent border-r-gray-800"></div>
          Clique para opcoes de acessibilidade
        </div>
      </button>
    </div>
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