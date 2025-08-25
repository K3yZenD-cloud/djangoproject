from django.contrib import admin
from .models import (
    Genre, Book, BookReview, Event, BlogPost, Member, 
    BookSuggestion, Newsletter, Gallery
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'reading_status', 'reading_start_date', 'average_rating']
    list_filter = ['reading_status', 'genres', 'publication_year']
    search_fields = ['title', 'author', 'isbn']
    filter_horizontal = ['genres']
    date_hierarchy = 'reading_start_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'author', 'isbn', 'publication_year')
        }),
        ('Contenido', {
            'fields': ('synopsis', 'cover_image', 'genres')
        }),
        ('Estado de Lectura', {
            'fields': ('reading_status', 'reading_start_date', 'reading_end_date')
        }),
        ('Calificación', {
            'fields': ('average_rating',)
        }),
    )

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'author_name', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['book__title', 'author_name', 'review_text']
    date_hierarchy = 'created_at'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'is_active']
    list_filter = ['event_type', 'is_active', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Fecha y Ubicación', {
            'fields': ('date', 'location', 'online_link')
        }),
        ('Detalles', {
            'fields': ('book', 'max_participants', 'is_active')
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'book', 'is_published', 'is_featured', 'created_at']
    list_filter = ['is_published', 'is_featured', 'created_at', 'book']
    search_fields = ['title', 'author_name', 'content']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'author_name', 'content')
        }),
        ('Relaciones', {
            'fields': ('book', 'featured_quote')
        }),
        ('Publicación', {
            'fields': ('is_published', 'is_featured')
        }),
    )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'join_date', 'is_active']
    list_filter = ['is_active', 'join_date', 'favorite_genres']
    search_fields = ['name', 'email', 'bio']
    filter_horizontal = ['favorite_genres']
    date_hierarchy = 'join_date'

@admin.register(BookSuggestion)
class BookSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'suggested_by_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'author', 'suggested_by_name', 'suggested_by_email']
    date_hierarchy = 'created_at'
    
    actions = ['approve_suggestions', 'reject_suggestions']
    
    def approve_suggestions(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} sugerencias aprobadas.")
    approve_suggestions.short_description = "Aprobar sugerencias seleccionadas"
    
    def reject_suggestions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} sugerencias rechazadas.")
    reject_suggestions.short_description = "Rechazar sugerencias seleccionadas"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    date_hierarchy = 'subscribed_at'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'is_featured', 'upload_date']
    list_filter = ['is_featured', 'upload_date', 'event']
    search_fields = ['title', 'description']
    date_hierarchy = 'upload_date'
