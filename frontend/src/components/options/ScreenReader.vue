<template>
  <div class="screen-reader-container">
    <label class="screen-reader-label">
      <div class="screen-reader-icon-wrapper">
        <svg xmlns="http://www.w3.org/2000/svg" class="screen-reader-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </div>
      <div class="screen-reader-content">
        <span class="screen-reader-title">Leitor de ecrã</span>
        <span class="screen-reader-subtitle">Narração de conteúdos</span>
      </div>
      <div class="screen-reader-toggle-wrapper">
        <input 
          type="checkbox"
          id="screen-reader"
          :checked="screenReader"
          @change="toggleScreenReader"
          class="sr-only"
        >
        <div class="screen-reader-toggle" :class="{'active': screenReader}">
          <div class="screen-reader-toggle-button" :class="{'active': screenReader}"></div>
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
.screen-reader-container {
  width: 100%;
  max-width: 100%;
  padding: clamp(0.5rem, 2vw, 0.75rem);
  background: #f1f5f9;
  border: 1px solid #64758b;
  border-radius: 0.5rem;
  transition: box-shadow 0.3s ease;
  box-sizing: border-box;
}

.screen-reader-container:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.screen-reader-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: clamp(0.5rem, 2vw, 0.75rem);
  width: 100%;
}

.screen-reader-icon-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.screen-reader-icon {
  width: clamp(1rem, 4vw, 1.5rem);
  height: clamp(1rem, 4vw, 1.5rem);
  color: #3b82f6;
}

.screen-reader-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.screen-reader-title {
  font-size: clamp(0.75rem, 3vw, 1rem);
  font-weight: 500;
  color: #1f2937;
  line-height: 1.2;
  word-wrap: break-word;
  hyphens: auto;
}

.screen-reader-subtitle {
  font-size: clamp(0.625rem, 2.5vw, 0.875rem);
  color: #64748b;
  line-height: 1.2;
  word-wrap: break-word;
  hyphens: auto;
}

.screen-reader-toggle-wrapper {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.screen-reader-toggle {
  position: relative;
  width: clamp(2rem, 5vw, 3.5rem);
  height: clamp(1rem, 2.5vw, 1.75rem);
  background: #d1d5db;
  border-radius: 9999px;
  transition: all 0.3s ease;
}

.screen-reader-toggle.active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.screen-reader-toggle-button {
  position: absolute;
  top: 0.125rem;
  left: 0.125rem;
  width: clamp(0.75rem, 2vw, 1.5rem);
  height: clamp(0.75rem, 2vw, 1.5rem);
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.screen-reader-toggle-button.active {
  transform: translateX(calc(clamp(2rem, 5vw, 3.5rem) - clamp(0.75rem, 2vw, 1.5rem) - 0.25rem));
  box-shadow: 0 3px 8px rgba(59, 130, 246, 0.3);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .screen-reader-container {
    background: #374151;
    border-color: #6b7280;
  }
  
  .screen-reader-title {
    color: #f9fafb;
  }
  
  .screen-reader-subtitle {
    color: #d1d5db;
  }
  
  .screen-reader-toggle {
    background: #4b5563;
  }
}

/* Breakpoint específico para dispositivos muito pequenos */
@media (max-width: 375px) {
  .screen-reader-container {
    padding: 0.5rem;
  }
  
  .screen-reader-label {
    gap: 0.5rem;
  }
  
  .screen-reader-content {
    gap: 0.0625rem;
  }
}

@media (max-width: 320px) {
  .screen-reader-container {
    padding: 0.375rem;
  }
  
  .screen-reader-label {
    gap: 0.375rem;
  }
}

/* Garante que nunca seja menor que o conteúdo mínimo */
@media (max-width: 280px) {
  .screen-reader-title {
    font-size: 0.65rem;
  }
  
  .screen-reader-subtitle {
    font-size: 0.55rem;
  }
}</style>