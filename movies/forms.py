from django import forms
from .models import MovieReview

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    
class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 100, 'style': 'background-color: #333;'}),
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu reseña aquí...', 'style': 'background-color: #333;'}),
        }