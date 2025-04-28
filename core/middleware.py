# class AccessibilityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         # Verifica se a resposta é HTML
#         if response.get('Content-Type', '').startswith('text/html'):
#             # Se for HTML, modifica para incluir o botão de acessibilidade
#             content = response.content.decode('utf-8')
            
#             # Insere o script e o container no final do body
#             if '</body>' in content:
#                 accessibility_button = '''
#                 <div id="accessibility-button-container"></div>
#                 <script src="/static/plugin_accessibility/js/accessibility-bundle.js"></script>
#                 <script>
#                     document.addEventListener('DOMContentLoaded', function() {
#                         initAccessibilityFeatures();
#                     });
#                 </script>
#                 '''
#                 content = content.replace('</body>', f'{accessibility_button}</body>')
#                 response.content = content.encode('utf-8')
                
#         return response

from django.utils.deprecation import MiddlewareMixin
from django.template.loader import render_to_string

class AccessibilityMiddleware(MiddlewareMixin):
    """
    Middleware que injeta o widget de acessibilidade em todas as respostas HTML
    """
    def process_response(self, request, response):
        if response.get('Content-Type', '').startswith('text/html'):
            if response.content:
                # Use o caminho correto para seus templates
                widget_html = render_to_string('core/core/accessibility_widget.html')
                
                # Se você tiver um template separado para scripts
                # scripts_html = render_to_string('core/core/accessibility_scripts.html')
                # widget_completo = widget_html + scripts_html
                # OU se estiver tudo em um único template:
                widget_completo = widget_html
                
                # Insere o widget antes da tag de fechamento do body
                response.content = response.content.replace(
                    b'</body>',
                    (widget_completo + '</body>').encode()
                )
        return response