from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Reading URLs
    path('lecturas/actual/', views.current_reading, name='current_reading'),
    path('lecturas/proximas/', views.upcoming_readings, name='upcoming_readings'),
    path('lecturas/sugerir/', views.suggest_book, name='suggest_book'),
    
    # Events URLs
    path('encuentros/', views.events, name='events'),
    path('encuentros/<int:pk>/', views.event_detail, name='event_detail'),
    
    # Library URL
    path('biblioteca/', views.library, name='library'),
    
    # Blog URLs
    path('reflexiones/', views.blog, name='blog'),
    path('reflexiones/<int:pk>/', views.blog_detail, name='blog_detail'),
    
    # Membership URLs
    path('unete/', views.join, name='join'),
    
    # Gallery URL
    path('galeria/', views.gallery, name='gallery'),
    
    # Newsletter subscription
    path('newsletter/suscribir/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
