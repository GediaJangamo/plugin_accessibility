from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    # name = 'plugin_siga_accessibility.core'

def ready(self):
        # Registra o middleware quando o app e carregado
        from django.conf import settings
        
        # Adiciona nosso middleware se ainda nao estiver na lista
        middleware_path = 'plugin_siga_accessibility.core.middleware.AccessibilityMiddleware'
        if middleware_path not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append(middleware_path)