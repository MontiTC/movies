import requests
from dotenv import load_dotenv
import os
from django.conf import settings
from movies.models import Person

load_dotenv("./.env")

KEY = os.getenv("API_KEY")
BASE_URL = 'https://api.themoviedb.org/3'

def get_actor_profile_path(person_id):
    url = f'{BASE_URL}/person/{person_id}?api_key={KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('profile_path')
    return None

def update_actor_profile_paths():
    actors = Person.objects.all()  # Obtén todos los actores de la base de datos
    for actor in actors:
        person_id = actor.tmdb_id  # Asegúrate de tener el ID de TMDb en tu modelo Person
        if person_id:
            profile_path = get_actor_profile_path(person_id)
            if profile_path:
                actor.profile_path = profile_path
                actor.save()
                print(f'Updated profile path for {actor.name}')
            else:
                print(f'No profile path found for {actor.name}')
        else:
            print(f'No TMDb ID for {actor.name}')

# Ejecutar la actualización
update_actor_profile_paths()