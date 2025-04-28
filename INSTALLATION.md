# Guia de Instalação do Plugin de Tecnologias Assistivas para o SIGA

Este documento apresenta o passo a passo completo para instalação e integração do Plugin de Tecnologias Assistivas em qualquer sistema baseado em Django e Python, desenvolvido como parte do trabalho "IMPLEMENTAÇÃO DE TECNOLOGIAS ASSISTIVAS NO SISTEMA INTEGRADO DE GESTÃO ACADÉMICA (SIGA): PROMOVENDO A INCLUSÃO DIGITAL DE ESTUDANTES COM DEFICIÊNCIA VISUAL".

## Requisitos Prévios

- Python 3.8 ou superior
- Django 3.2 ou superior
- pip (gerenciador de pacotes Python)
- Um projeto Django existente onde o plugin será instalado

## 1. Instalação do Plugin

### 1.1 Instalação Direta via GitHub

```bash
# Instale o plugin diretamente do repositório GitHub
pip install git+https://github.com/GediaJangamo/plugin_accessibility.git
```

### 1.2 Instalação Local (opcional)

Se preferir instalar a partir de uma cópia local:

```bash
# Clone o repositório
git clone https://github.com/GediaJangamo/plugin_accessibility.git

# Entre no diretório do projeto
cd plugin_siga_accessibility

# Instale em modo de desenvolvimento
pip install -e .
```

## 2. Configuração do Projeto Django

### 2.1 Adicione o Plugin aos Aplicativos Instalados

Abra o arquivo `settings.py` do seu projeto Django e adicione o plugin à lista `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... apps existentes
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Adicione o plugin de acessibilidade
    'plugin_siga_accessibility.core',
]
```

### 2.2 Adicione o Middleware de Acessibilidade

Adicione o middleware ao seu arquivo `settings.py`:

```python
MIDDLEWARE = [
    # ... middlewares existentes
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Adicione o middleware de acessibilidade
    'plugin_siga_accessibility.core.middleware.AccessibilityMiddleware',
]
```

### 2.3 Configure os Arquivos Estáticos

Certifique-se de que a configuração de arquivos estáticos esteja correta no seu `settings.py`:

```python
STATIC_URL = '/static/'

# Adicione isto se ainda não estiver configurado
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

## 3. Coletando Arquivos Estáticos

Para garantir que todos os arquivos estáticos do plugin estejam disponíveis:

```bash
python manage.py collectstatic
```

## 4. Verificação da Instalação

Para verificar se o plugin foi instalado corretamente:

1. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

2. Acesse qualquer página do seu sistema no navegador.
   O botão de acessibilidade deve aparecer automaticamente em todas as páginas.

## 5. Configurações Específicas de Acessibilidade (Opcional)

Adicione ao seu arquivo `settings.py`:

```python
# Configurações do plugin de acessibilidade
ACCESSIBILITY_SETTINGS = {
    'enable_screen_reader': True,
    'enable_high_contrast': True,
    'enable_text_zoom': True,
    'default_font_size': 16,
    'button_position': 'bottom-right',  # bottom-right, bottom-left, top-right, top-left
}
```

## 6. Personalização (Opcional)

### 6.1 Personalizando a Aparência do Botão

Para personalizar a aparência do botão de acessibilidade, você pode sobrescrever as configurações padrão:

```python
# settings.py
ACCESSIBILITY_BUTTON_STYLE = {
    'background_color': '#0066cc',
    'icon_color': '#ffffff',
    'border_radius': '50%',
    'size': '60px',
}
```

### 6.2 Excluindo o Botão de Páginas Específicas

Se você deseja que o botão não apareça em determinadas páginas:

```python
# settings.py
ACCESSIBILITY_EXCLUDE_PATHS = [
    '/admin/',
    '/reports/exports/',
]
```

## 7. Resolução de Problemas Comuns

### 7.1 O Botão Não Aparece

Se o botão de acessibilidade não estiver aparecendo:

1. Verifique se o `collectstatic` foi executado corretamente
2. Confirme que o middleware está registrado na lista `MIDDLEWARE`
3. Verifique se há erros no console do navegador

### 7.2 Conflitos com JavaScript Existente

Se o plugin estiver causando conflitos com outros scripts:

1. Certifique-se de que o plugin é carregado após bibliotecas como jQuery
2. Verifique o console do navegador para identificar possíveis erros
3. Use as configurações `ACCESSIBILITY_SETTINGS` para ajustar o comportamento

### 7.3 Problemas de Compatibilidade com Templates

Se seu projeto usa um sistema de templates diferente ou framework front-end:

1. Você pode implementar manualmente a inclusão do botão adicionando este código ao seu template base:

```html
<div id="accessibility-button-container"></div>
<script src="{% static 'plugin_accessibility/js/accessibility-bundle.js' %}"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        initAccessibilityFeatures();
    });
</script>
```

## 8. Suporte e Atualizações

Para obter suporte ou reportar problemas, visite o repositório do projeto:
https://github.com/seu-usuario/plugin_siga_accessibility

---

Este plugin foi desenvolvido como parte de um Trabalho de Conclusão de Curso, com o objetivo de promover a inclusão digital de estudantes com deficiência visual no Sistema Integrado de Gestão Acadêmica (SIGA).