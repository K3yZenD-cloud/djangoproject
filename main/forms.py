from django import forms
from .models import BookSuggestion, Member, Newsletter

class BookSuggestionForm(forms.ModelForm):
    class Meta:
        model = BookSuggestion
        fields = ['title', 'author', 'suggested_by_name', 'suggested_by_email', 'reason']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del libro'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Autor del libro'
            }),
            'suggested_by_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre'
            }),
            'suggested_by_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '¿Por qué recomiendas este libro? ¿Qué lo hace especial?'
            }),
        }
        labels = {
            'title': 'Título del Libro',
            'author': 'Autor',
            'suggested_by_name': 'Tu Nombre',
            'suggested_by_email': 'Tu Email',
            'reason': 'Razón de la Recomendación',
        }

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'bio', 'favorite_genres']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos un poco sobre ti, tus gustos literarios, qué esperas del club...'
            }),
            'favorite_genres': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'name': 'Nombre Completo',
            'email': 'Email',
            'phone': 'Teléfono (opcional)',
            'bio': 'Presentación',
            'favorite_genres': 'Géneros Favoritos',
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        }),
        label='Nombre'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        }),
        label='Email'
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Asunto del mensaje'
        }),
        label='Asunto'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...'
        }),
        label='Mensaje'
    )

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre (opcional)'
            }),
        }
        labels = {
            'email': 'Email',
            'name': 'Nombre',
        }
