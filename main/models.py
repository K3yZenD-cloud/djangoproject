from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

class Book(models.Model):
    READING_STATUS_CHOICES = [
        ('current', 'Lectura Actual'),
        ('upcoming', 'Próxima Lectura'),
        ('completed', 'Completado'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=200, verbose_name="Autor")
    isbn = models.CharField(max_length=13, blank=True, verbose_name="ISBN")
    publication_year = models.IntegerField(blank=True, null=True, verbose_name="Año de Publicación")
    synopsis = models.TextField(verbose_name="Sinopsis")
    cover_image = models.URLField(blank=True, verbose_name="URL de Portada")
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Géneros")
    reading_status = models.CharField(max_length=20, choices=READING_STATUS_CHOICES, default='upcoming', verbose_name="Estado de Lectura")
    reading_start_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Inicio")
    reading_end_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Finalización")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Calificación Promedio")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['-created_at']

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100, verbose_name="Nombre del Autor")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Calificación")
    review_text = models.TextField(verbose_name="Reseña")
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="Destacada")
    
    def __str__(self):
        return f"Reseña de {self.book.title} por {self.author_name}"
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('meeting', 'Reunión del Club'),
        ('discussion', 'Discusión de Libro'),
        ('author_talk', 'Charla con Autor'),
        ('workshop', 'Taller'),
        ('other', 'Otro'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='meeting', verbose_name="Tipo de Evento")
    date = models.DateTimeField(verbose_name="Fecha y Hora")
    location = models.CharField(max_length=200, blank=True, verbose_name="Ubicación")
    online_link = models.URLField(blank=True, verbose_name="Enlace Online")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Libro Relacionado")
    max_participants = models.IntegerField(blank=True, null=True, verbose_name="Máximo de Participantes")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('main:event_detail', kwargs={'pk': self.pk})
    
    @property
    def is_past(self):
        return self.date < timezone.now()
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['date']

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    author_name = models.CharField(max_length=100, verbose_name="Autor")
    content = models.TextField(verbose_name="Contenido")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Libro Relacionado")
    featured_quote = models.TextField(blank=True, verbose_name="Cita Destacada")
    is_published = models.BooleanField(default=True, verbose_name="Publicado")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main:blog_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Entrada de Blog"
        verbose_name_plural = "Entradas de Blog"
        ordering = ['-created_at']

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    bio = models.TextField(blank=True, verbose_name="Biografía")
    favorite_genres = models.ManyToManyField(Genre, blank=True, verbose_name="Géneros Favoritos")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    profile_image = models.URLField(blank=True, verbose_name="Foto de Perfil")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        ordering = ['name']

class BookSuggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=200, verbose_name="Autor")
    suggested_by_name = models.CharField(max_length=100, verbose_name="Sugerido por")
    suggested_by_email = models.EmailField(verbose_name="Email del Sugerente")
    reason = models.TextField(verbose_name="Razón de la Sugerencia")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.author} (sugerido por {self.suggested_by_name})"
    
    class Meta:
        verbose_name = "Sugerencia de Libro"
        verbose_name_plural = "Sugerencias de Libros"
        ordering = ['-created_at']

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nombre")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Suscriptor Newsletter"
        verbose_name_plural = "Suscriptores Newsletter"

class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    image_url = models.URLField(verbose_name="URL de Imagen")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Evento Relacionado")
    upload_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="Destacada")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Galería"
        ordering = ['-upload_date']
