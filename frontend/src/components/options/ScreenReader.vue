<template>
  <div class="p-2 sm:p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
    <label class="flex items-center cursor-pointer gap-2 sm:gap-3">
      <div class="flex-shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-[#3b82f6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </div>
      <div class="flex-grow min-w-0 flex-1">
        <span class="block text-sm sm:text-base md:text-lg text-gray-800 dark:text-white font-medium truncate">Leitor de ecrã</span>
        <span class="text-xs sm:text-sm text-[#64748b] dark:text-gray-300 truncate">Narração de conteúdos</span>
      </div>
      <div class="flex items-center flex-shrink-0">
        <input 
          type="checkbox"
          id="screen-reader"
          :checked="screenReader"
          @change="toggleScreenReader"
          class="sr-only"
        >
        <div class="relative w-10 h-5 sm:w-12 sm:h-6 md:w-14 md:h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-blue-500': screenReader}">
          <div class="absolute left-0.5 top-0.5 bg-white w-4 h-4 sm:w-5 sm:h-5 rounded-full shadow transition duration-300 ease-in-out transform" :class="{'translate-x-5 sm:translate-x-6 md:translate-x-7': screenReader}"></div>
        </div>
      </div>
    </label>
         
    <!-- Teleport para colocar o controle do leitor de tela no final do body -->
    <teleport to="body">
      <ScreenReaderControl :active="screenReader" @update:screenReader="updateScreenReader" />
    </teleport>
  </div>
</template>

<script>
import ScreenReaderControl from '../controller/ScreenReaderControl.vue';

export default {
  name: 'ScreenReader',
  components: {
    ScreenReaderControl
  },
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
      this.$emit('announce', newValue ? 'Leitor de ecrã activado' : 'Leitor de ecrã desactivado');
    },
    
    updateScreenReader(value) {
      this.$emit('update:screenReader', value);
    }
  }
}
</script>

<style scoped>
/* Animação suave para o switch */
input:checked + div {
  background: linear-gradient(135deg, #3b82f6);
}

input:checked + div > div {
  box-shadow: 0 3px 8px #3b82f6;
}
</style>
