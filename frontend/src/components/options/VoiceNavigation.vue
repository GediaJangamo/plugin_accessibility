<!-- Navegacao por voz -->
  <template>
    <div class="p-3 bg-[#f1f5f9] border-[#64758b] dark:bg-gray-800 rounded-lg hover:shadow-md transition-shadow duration-300">
      <label class="flex items-center cursor-pointer">
        <div class="flex-shrink-0 mr-4">
          <!-- <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg> -->
          <svg 
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-7 w-7 text-[#3b82f6] ">
          <circle cx="10" cy="6" r="4" />
          <path d="M19 2C19 2 21 3.2 21 6C21 8.8 19 10 19 10" />
          <path d="M17 4C17 4 18 4.6 18 6C18 7.4 17 8 17 8" />
          <path d="M17.9975 18C18 17.8358 18 17.669 18 17.5C18 15.0147 14.4183 13 10 13C5.58172 13 2 15.0147 2 17.5C2 19.9853 2 22 10 22C12.231 22 13.8398 21.8433 15 21.5634" />
        </svg>

        </div>
        <div class="flex-grow">
          <span class="block text-lg text-gray-800 dark:text-white font-medium">Comandos de Voz</span>
          <span class="text-sm text-[#64748b] dark:text-gray-300">Navegue com a sua voz</span>
        </div>
        <div class="flex items-center">
          <input
            type="checkbox"
            id="voice-commands"
            :checked="voiceCommands"
            @change="toggleVoiceCommands"
            class="sr-only"
          >
          <div class="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full transition duration-300 ease-in-out" :class="{'bg-blue-500': voiceCommands}">
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
