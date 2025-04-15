<template>
  <div>
    <accessibility-button @toggle-menu="toggleMenu"></accessibility-button>
    <accessibility-menu :is-open="menuOpen"></accessibility-menu>
  </div>
</template>

<script>
import AccessibilityButton from './components/AccessibilityButton.vue'
import AccessibilityMenu from './components/AccessibilityMenu.vue'

export default {
  name: 'App',
  components: {
    AccessibilityButton,
    AccessibilityMenu
  },
  data() {
    return {
      menuOpen: false
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen
    }
  }
}
</script> 

