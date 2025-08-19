<template>
  <div class="container">
    <label class="label">
      <div class="icon-wrapper">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </div>
      <div class="content">
        <span class="title">Leitor de ecrã</span>
        <span class="subtitle">Narração de conteúdos</span>
      </div>
      <div class="toggle-wrapper">
        <input 
          type="checkbox"
          id="screen-reader"
          :checked="screenReader"
          @change="toggleScreenReader"
          class="sr-only"
        >
        <div class="toggle" :class="{'active': screenReader}">
          <div class="toggle-button" :class="{'active': screenReader}"></div>
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
.container {
  padding: 8px;
  background: #f1f5f9;
  border: 1px solid #64758b;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
  margin: 4px;
  min-width: 0;
  overflow: hidden;
}

.container:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.label {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 8px;
  min-width: 0;
}

.icon-wrapper {
  flex-shrink: 0;
}

.icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.content {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.title {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.subtitle {
  display: block;
  font-size: 12px;
  color: #64748b;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toggle-wrapper {
  flex-shrink: 0;
}

.toggle {
  position: relative;
  width: 40px;
  height: 20px;
  background: #d1d5db;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.toggle.active {
  background: #3b82f6;
}

.toggle-button {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.toggle-button.active {
  transform: translateX(20px);
  box-shadow: 0 3px 8px rgba(59, 130, 246, 0.3);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Mobile pequeno */
@media (max-width: 400px) {
  .container {
    padding: 6px;
    margin: 2px;
  }
  
  .label {
    gap: 6px;
  }
  
  .icon {
    width: 18px;
    height: 18px;
  }
  
  .title {
    font-size: 13px;
  }
  
  .subtitle {
    font-size: 11px;
  }
  
  .toggle {
    width: 36px;
    height: 18px;
  }
  
  .toggle-button {
    width: 14px;
    height: 14px;
  }
  
  .toggle-button.active {
    transform: translateX(18px);
  }
}

/* Mobile muito pequeno */
@media (max-width: 320px) {
  .container {
    padding: 4px;
    margin: 1px;
  }
  
  .label {
    gap: 4px;
  }
  
  .icon {
    width: 16px;
    height: 16px;
  }
  
  .title {
    font-size: 12px;
  }
  
  .subtitle {
    font-size: 10px;
  }
  
  .toggle {
    width: 32px;
    height: 16px;
  }
  
  .toggle-button {
    width: 12px;
    height: 12px;
  }
  
  .toggle-button.active {
    transform: translateX(16px);
  }
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .container {
    background: #374151;
    border-color: #6b7280;
  }
  
  .title {
    color: #f9fafb;
  }
  
  .subtitle {
    color: #d1d5db;
  }
  
  .toggle {
    background: #4b5563;
  }
}</style>