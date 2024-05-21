from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieCredit, Person
from .forms import MovieReviewForm, MovieReview
# Create your views here.
from .forms import NameForm
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q

def get_name(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            
            return render(request, "movies/name_ok.html", {"form": form})
        else:
            return render(request, "movies/name_ok.html", {"form": form})
    else:
        form = NameForm()
    return render(request, "movies/name.html", {"form": form})

def index(request):
    movies = Movie.objects.all().order_by('title')
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)
    #return HttpResponse(movies)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.moviereview_set.all()
    credits = MovieCredit.objects.filter(movie=movie)[:5]

    # Fetch recommended movies based on the genres of the current movie
    genre_ids = [genre.id for genre in movie.genres.all()]
    recommended_movies = Movie.objects.filter(
        ~Q(id=movie_id) & (Q(genres__in=movie.genres.all()) | Q(genres__isnull=True))
    ).distinct().exclude(genres__id__in=[g.id for g in movie.genres.exclude(id__in=genre_ids)])[:5]

    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = MovieReviewForm()

    genres = movie.genres.all()
    context = {'movie': movie, 'genres': genres, 'form': form, 'reviews': reviews, 'credits': credits, 'recommended_movies': recommended_movies}
    return render(request, "movies/movie_detail.html", context)
# views.py
def create_review(request, movie_id):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id  # Asignar movie_id aquí
            review.save()
            return index(request)
    else:
        form = MovieReviewForm()
    return render(request, 'create_review.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render('movies/index.html')
    else:
        return render(request, 'movies/index.html')

from django.http import JsonResponse
from .models import Person


def actor_movies(request, actor_id):
    actor = get_object_or_404(Person, pk=actor_id)
    movies = actor.movie_set.all()  # Consulta todas las películas en las que participa el actor
    return render(request, 'movies/actor_movies.html', {'movies': movies, 'actor': actor})
    
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'movies/login.html'
