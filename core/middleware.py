class AccessibilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Verifica se a resposta é HTML
        if response.get('Content-Type', '').startswith('text/html'):
            # Se for HTML, modifica para incluir o botão de acessibilidade
            content = response.content.decode('utf-8')
            
            # Insere o script e o container no final do body
            if '</body>' in content:
                accessibility_button = '''
                <div id="accessibility-button-container"></div>
                <script src="/static/plugin_accessibility/js/accessibility-bundle.js"></script>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        initAccessibilityFeatures();
                    });
                </script>
                '''
                content = content.replace('</body>', f'{accessibility_button}</body>')
                response.content = content.encode('utf-8')
                
        return response