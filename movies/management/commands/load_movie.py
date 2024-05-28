from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime
import requests
import random
import json
import os

Authorization = f"Bearer {os.getenv('TOKEN')}"

class Command(BaseCommand):
    # help = "Loads a movie, we assume the database is empty"

    def handle(self, *args, **options):
        # Remove all movies from db
        Movie.objects.all().delete()
        
        
        for i in range(1, 100):
            random_id = random.randint(1, 1000000)
            print(f"Loading movie {i}, TMDB ID: {random_id}")
            url = f"https://api.themoviedb.org/3/movie/{random_id}?language=en-US"

            headers = {
                "accept": "application/json",
                "Authorization": Authorization
            }

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                continue
        
            # Checks if the movie is for adults
            if response.json()["adult"]:
                continue
            
            # Checks if release date is empty
            
            if response.json()["release_date"] == "":
                continue
            
            
            # Checks if poster path is null
            poster = response.json()["poster_path"]
            
            if poster is None:
                poster = "https://res.cloudinary.com/teepublic/image/private/s--4ydOGeR1--/c_crop,x_10,y_10/c_fit,h_1109/c_crop,g_north_west,h_1260,w_1260,x_-76,y_-76/co_rgb:ffffff,e_colorize,u_Misc:One%20Pixel%20Gray/c_scale,g_north_west,h_1260,w_1260/fl_layer_apply,g_north_west,x_-76,y_-76/bo_157px_solid_white/e_overlay,fl_layer_apply,h_1260,l_Misc:Art%20Print%20Bumpmap,w_1260/e_shadow,x_6,y_6/c_limit,h_1254,w_1254/c_lpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_auto:good:420,w_630/v1689330389/production/designs/47836837_1.jpg"
            else:
                poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster}"
                
                            
            # Create a new movie object
            movie = Movie(
                title=response.json()["title"],
                overview=response.json()["overview"],
                release_date=datetime.strptime(response.json()["release_date"], "%Y-%m-%d"),
                running_time=response.json()["runtime"],
                budget=response.json()["budget"],
                tmdb_id=response.json()["id"],
                revenue=response.json()["revenue"],
                poster_path=poster,
                # genres=genres_to_store,
                # credits=movie_credits
            )
            
            movie.save()
            
            
            # From the genres got in the response, compare it with my DB and return the genre object
            genres = response.json()["genres"]
            genres_to_store = []
            for genre in genres:
                genre_obj = Genre.objects.filter(name=genre["name"]).first()
                # If not found, create a new genre object
                if genre_obj is None:
                    genre_obj = Genre(name=genre["name"])
                    genre_obj.save()
                    
                genres_to_store.append(genre_obj)
            
            # Add genres to movie
            movie.genres.set(genres_to_store)
            
            # Get credits and add it to the DB
            credits = get_credits(random_id)
            persons = []
            # API returns two lists
            for credit in credits["cast"]:
                persons.append(create_credit(credit["name"], movie, "Actor")[0])
            
            for credit in credits["crew"]:
                persons.append(create_credit(credit["name"], movie, credit["job"])[0])
                
            # Add the credits to the movie object
            movie.credits.set(persons)
            
        
        # print(Movie.objects.all())
            
def get_credits(movie_id):
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    
    headers = {
        "accept": "application/json",
        "Authorization": Authorization
    }

    response = requests.get(url, headers=headers)

    return response.json()

def create_credit(person_name, movie, job):
    person = Person.objects.filter(name=person_name).first()
    # If the person is not in the DB, create a new person object
    if person is None:
        person = Person(name=person_name)
        person.save()
        
    job_obj = Job.objects.filter(name=job).first()
    # If the job is not in the DB, create a new job object
    if job_obj is None:
        job_obj = Job(name=job)
        job_obj.save()
        
    # Create a new MovieCredit object 
    credit = MovieCredit(person=person, movie=movie, job=job_obj)
    credit.save()
    
    # Returns tuple to give flexibility to the caller
    return (person, job_obj, credit)
