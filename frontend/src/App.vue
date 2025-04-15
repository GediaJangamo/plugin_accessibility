<template>
  <div>
    <accessibility-component></accessibility-component>
    <main id="main-content">
      <!-- Your main content here -->
    </main>
  </div>
</template>

<script>
import AccessibilityComponent from './components/AccessibilityComponent.vue';

export default {
  name: 'App',
  components: {
    AccessibilityComponent
  }
}
</script>