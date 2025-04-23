<!-- Navegacao por voz -->
  <template>
    <div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Comandos por Voz</span>
          <span class="text-sm text-gray-600 dark:text-gray-300">Navegue com sua voz</span>
        </div>
        <div class="flex items-center">
          <input
            type="checkbox"
            id="voice-commands"
            :checked="voiceCommands"
            @change="toggleVoiceCommands"
            class="sr-only"
          >
          <div class="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-green-500': voiceCommands}">
            <div class="absolute left-1 top-1 bg-white w-5 h-5 rounded-full shadow transition duration-300 ease-in-out" :class="{'transform translate-x-7': voiceCommands}"></div>
          </div>
        </div>
      </label>
      
      <!-- Teleport para colocar o controle de voz no final do body -->
      <teleport to="body">
        <VoiceCommandController 
          :active="voiceCommands" 
          @announce="announceMessage"
          @executeCommand="handleCommand"
        />
      </teleport>
    </div>
  </template>
  
  <script>
  import VoiceCommandController from '../controller/VoiceCommandController.vue';
  
  export default {
    name: 'VoiceNavigation',
    components: {
      VoiceCommandController
    },
    props: {
      voiceCommands: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      toggleVoiceCommands() {
        const newValue = !this.voiceCommands;
        this.$emit('update:voiceCommands', newValue);
      },
      
      announceMessage(message) {
        this.$emit('announce', message);
      },
      
      handleCommand(command) {
        this.$emit('executeCommand', command);
      }
    }
  }
  </script>