from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Vista principal de la aplicación"""
    return render(request, 'main/home.html')

def about(request):
    """Vista de información sobre la aplicación"""
    return render(request, 'main/about.html')

def contact(request):
    """Vista de contacto"""
    return render(request, 'main/contact.html')
