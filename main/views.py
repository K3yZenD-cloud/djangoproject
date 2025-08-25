from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Book, Event, BlogPost, Member, BookSuggestion, Newsletter, Gallery, Genre, BookReview
from .forms import BookSuggestionForm, MemberRegistrationForm, ContactForm, NewsletterForm

def home(request):
    """Vista principal de la aplicación"""
    current_book = Book.objects.filter(reading_status='current').first()
    upcoming_events = Event.objects.filter(date__gte=timezone.now(), is_active=True)[:3]
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:2]
    featured_quote = BlogPost.objects.filter(is_published=True, featured_quote__isnull=False).exclude(featured_quote='').first()
    
    context = {
        'current_book': current_book,
        'upcoming_events': upcoming_events,
        'featured_posts': featured_posts,
        'featured_quote': featured_quote,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """Vista de información sobre la aplicación"""
    members = Member.objects.filter(is_active=True)[:6]
    context = {
        'members': members,
    }
    return render(request, 'main/about.html', context)

def current_reading(request):
    """Vista de la lectura actual"""
    current_book = Book.objects.filter(reading_status='current').first()
    reviews = BookReview.objects.filter(book=current_book)[:5] if current_book else []
    
    context = {
        'current_book': current_book,
        'reviews': reviews,
    }
    return render(request, 'main/current_reading.html', context)

def upcoming_readings(request):
    """Vista de próximas lecturas"""
    upcoming_books = Book.objects.filter(reading_status='upcoming').order_by('reading_start_date')
    
    context = {
        'upcoming_books': upcoming_books,
    }
    return render(request, 'main/upcoming_readings.html', context)

def suggest_book(request):
    """Vista para sugerir libros"""
    if request.method == 'POST':
        form = BookSuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias por tu sugerencia! La revisaremos pronto.')
            return redirect('main:suggest_book')
    else:
        form = BookSuggestionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/suggest_book.html', context)

def events(request):
    """Vista de eventos y actividades"""
    upcoming_events = Event.objects.filter(date__gte=timezone.now(), is_active=True).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')[:6]
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'main/events.html', context)

def event_detail(request, pk):
    """Vista detalle de evento"""
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'main/event_detail.html', context)

def library(request):
    """Vista de biblioteca recomendada"""
    genre_filter = request.GET.get('genre')
    search_query = request.GET.get('search')
    
    books = Book.objects.filter(reading_status='completed').order_by('-reading_end_date')
    
    if genre_filter:
        books = books.filter(genres__name=genre_filter)
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    genres = Genre.objects.all()
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'current_genre': genre_filter,
        'search_query': search_query,
    }
    return render(request, 'main/library.html', context)

def blog(request):
    """Vista del blog/reflexiones"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/blog.html', context)

def blog_detail(request, pk):
    """Vista detalle de entrada de blog"""
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    related_posts = BlogPost.objects.filter(
        is_published=True, 
        book=post.book
    ).exclude(pk=pk)[:3] if post.book else []
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'main/blog_detail.html', context)

def join(request):
    """Vista para unirse al club"""
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Bienvenido al Club de Lectura ELIXIR! Te contactaremos pronto.')
            return redirect('main:join')
    else:
        form = MemberRegistrationForm()
    
    recent_members = Member.objects.filter(is_active=True).order_by('-join_date')[:6]
    
    context = {
        'form': form,
        'recent_members': recent_members,
    }
    return render(request, 'main/join.html', context)

def gallery(request):
    """Vista de galería"""
    images = Gallery.objects.all().order_by('-upload_date')
    featured_images = images.filter(is_featured=True)[:6]
    
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'featured_images': featured_images,
    }
    return render(request, 'main/gallery.html', context)

def contact(request):
    """Vista de contacto"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email
            messages.success(request, '¡Mensaje enviado! Te responderemos pronto.')
            return redirect('main:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/contact.html', context)

def newsletter_subscribe(request):
    """Vista para suscribirse al newsletter"""
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        
        if email:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
            
            if created:
                return JsonResponse({'success': True, 'message': '¡Suscripción exitosa!'})
            else:
                return JsonResponse({'success': False, 'message': 'Este email ya está suscrito.'})
    
    return JsonResponse({'success': False, 'message': 'Error en la suscripción.'})
