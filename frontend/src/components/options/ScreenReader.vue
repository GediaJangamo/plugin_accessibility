<template>
  <div class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 mx-2 sm:mx-0">
    <!-- Cabeçalho -->
    <div class="mb-4">
      <h2 class="text-xl font-bold text-gray-800 dark:text-white">SISTEMA INTEGRADO DE GESTÃO ACADÊMICA</h2>
    </div>
    
    <!-- Conteúdo principal -->
    <div class="space-y-4 text-gray-700 dark:text-gray-300">
      <p class="text-base leading-relaxed">
        Caro estudante, por motivos de segurança os seus dados de acesso ao SIGA 2.0 foram actualizados.
      </p>
      
      <p class="text-base leading-relaxed">
        Neste sentido, para aceder ao sistema deverá usar como user name o seu e-mail de estudante da UEM e como password o seu nr. de estudante, isto é:
      </p>
      
      <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
        <div class="mb-3">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Username:</label>
          <div class="text-sm bg-gray-100 dark:bg-gray-600 p-2 rounded">
            colocar seu e-mail na forma xxxxxx@uem.ac.nz
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password:</label>
          <div class="text-sm bg-gray-100 dark:bg-gray-600 p-2 rounded">
            colocar seu nr de estudante
          </div>
        </div>
      </div>
      
      <div class="mt-4">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email do utilizador</label>
        <input 
          type="email" 
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="xxxxxx@uem.ac.nz"
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginInfoCard'
}
</script>

<style scoped>
/* Garante que o texto quebre corretamente em mobile */
@media (max-width: 640px) {
  .text-base {
    word-break: break-word;
    overflow-wrap: break-word;
  }
}
</style>