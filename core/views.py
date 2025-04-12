from django.shortcuts import render

def home(request):
    """Pagina Inicial-botao acessivel"""
    return render(request, 'core/base.html')
  

