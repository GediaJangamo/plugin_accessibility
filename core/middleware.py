from django.utils.deprecation import MiddlewareMixin
from django.template.loader import render_to_string

class AccessibilityMiddleware(MiddlewareMixin):
    """
    Middleware que injeta o widget de acessibilidade em todas as respostas HTML
    """
    def process_response(self, request, response):
        if response.get('Content-Type', '').startswith('text/html'):
            if response.content:
               
                widget_html = render_to_string('core/base.html')
            
                widget_completo = widget_html
                
                response.content = response.content.replace(
                    b'</body>',
                    (widget_completo + '</body>').encode()
                )
        return response