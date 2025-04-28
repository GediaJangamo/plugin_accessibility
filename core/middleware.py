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
                widget_html = render_to_string('core/base.html')
            
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