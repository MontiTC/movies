document.addEventListener('DOMContentLoaded', function() {
    const actorItems = document.querySelectorAll('.actor-item');
    const actorMoviesContainer = document.getElementById('actor-movies-container');

    actorItems.forEach(function(actorItem) {
        actorItem.addEventListener('click', function() {
            const actorId = this.getAttribute('data-actor-id');
            global fetch(`/api/actor/${actorId}/movies`)
                .then(response => response.json())
                .then(data => {
                    const movies = data.movies;
                    const moviesList = movies.map(movie => `<li>${movie.title}</li>`).join('');
                    actorMoviesContainer.innerHTML = `<h2>Movies of ${this.textContent}</h2><ul>${moviesList}</ul>`;
                })
                .catch(error => console.error('Error fetching actor movies:', error));
        });
    });
});