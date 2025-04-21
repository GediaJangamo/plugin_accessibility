<!-- CursorCustomizer -->
<template>
  <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
    <div class="flex items-center mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
      </svg>
      <h3 class="font-medium text-lg text-gray-800 dark:text-white">Cursor</h3>
    </div>
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Amplie o cursor e altere a sua cor</p>
    <div class="flex gap-3">
      <button 
        @click="setCursorColor('white')" 
        class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium text-lg"
        :class="cursorColor === 'white' ? 'ring-2 ring-[#077b4b] bg-white text-black' : 'bg-white text-black'"
      >
        BRANCO
      </button>
      <button 
        @click="setCursorColor('black')" 
        class="flex-1 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md font-medium text-lg"
        :class="cursorColor === 'black' ? 'ring-2 ring-[#077b4b] bg-gray-900 text-white' : 'bg-gray-900 text-white'"
      >
        PRETO
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CursorCustomizer',
  props: {
    cursorColor: {
      type: String,
      default: 'black'
    }
  },
  watch: {
    cursorColor: {
      immediate: true,
      handler(newValue) {
        this.applyCursorColor(newValue);
      }
    }
  },
  mounted() {
    this.addCursorStyles();
  },
  methods: {
    setCursorColor(color) {
      this.$emit('update:cursorColor', color);
    },
    
    applyCursorColor(color) {
      document.body.classList.remove('cursor-color-black', 'cursor-color-white');
      document.body.classList.add(`cursor-color-${color}`);
    },
    
addCursorStyles() {
  const styleEl = document.createElement('style');
  styleEl.innerHTML = `
    body.cursor-color-white * {
      cursor: url('/static/core/img/hand_cursor_whiteSmall.png') 10 10, pointer !important;
    }

    body.cursor-color-black * {
      cursor: url('/static/core/img/hand_cursor_black.png') 10 10, pointer !important;
    }
  `;
  document.head.appendChild(styleEl);
}

  }
}
</script>