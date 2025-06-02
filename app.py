import os
import requests
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, request
from omdb_utils import fetch_omdb_data
from datamanager.sqlite_data_manager import SQLiteDataManager

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)


@app.route('/')
def home_redirect():
    """Landing page for the app with retro theme."""
    return render_template('landing.html')


@app.route('/users')
def list_users():
    """Render the page that lists all users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Handle user addition.

    GET: Render the add user form.
    POST: Add a new user and redirect to the user list.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            data_manager.add_user(name)
            return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Render the page displaying movies for a specific user.

    Args:
        user_id: The ID of the user.
    """
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Redirect old add_movie route to the fuzzy search flow."""
    return redirect(url_for('add_movie_search', user_id=user_id))

@app.route('/users/<int:user_id>/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(user_id, movie_id):
    """Allow manual editing of a movie's data without fetching from OMDb."""
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if not user or not movie or movie.user_id != user.id:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title') or movie.title
        director = request.form.get('director') or movie.director
        year = request.form.get('year') or movie.year
        rating = request.form.get('rating') or movie.rating
        poster_url = request.form.get('poster_url') or movie.poster_url
        plot = request.form.get('plot') or movie.plot

        data_manager.update_movie(movie_id, title, director, year, rating, poster_url, plot)
        return redirect(url_for('user_movies', user_id=user.id))

    return render_template('edit_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """Handle deleting a movie for a user.

    Args:
        user_id: The ID of the user.
        movie_id: The ID of the movie to delete.
    """
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if not user or not movie or movie.user_id != user.id:
        abort(404)

    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user.id))

@app.route('/users/<int:user_id>/add_movie_search', methods=['GET', 'POST'])
def add_movie_search(user_id):
    """Render a search form for movie titles and display matching OMDb results."""
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    search_results = []
    title = ""

    if request.method == 'POST':
        title = request.form.get('title')
        api_key = os.getenv('OMDB_API_KEY')
        try:
            url = f'http://www.omdbapi.com/?apikey={api_key}&s={title}'
            response = requests.get(url)
            data = response.json()
            if data.get('Search'):
                search_results = data['Search']
        except:
            pass

    return render_template('search_movie.html', user=user, search_results=search_results, title=title)


@app.route('/users/<int:user_id>/confirm_add_movie/<imdb_id>', methods=['GET', 'POST'])
def confirm_add_movie(user_id, imdb_id):
    """Display a confirmation form with movie data from OMDb, then add to database."""
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    api_key = os.getenv('OMDB_API_KEY')
    url = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
    response = requests.get(url)
    data = response.json()

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director') or ''
        year = request.form.get('year') or ''
        rating = request.form.get('rating') or ''
        poster_url = request.form.get('poster_url') or ''
        plot = request.form.get('plot') or ''

        data_manager.add_movie(user_id, title, director, year, rating, poster_url, plot)
        return redirect(url_for('user_movies', user_id=user.id))

    return render_template('confirm_add_movie.html', user=user, movie=data)


@app.route('/users/<int:user_id>/edit_movie_search/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie_search(user_id, movie_id):
    """Search for a new movie title to update an existing movie."""
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)
    if not user or not movie or movie.user_id != user.id:
        abort(404)

    search_results = []
    title = request.args.get('title', movie.title)

    if request.method == 'POST':
        title = request.form.get('title')
        api_key = os.getenv('OMDB_API_KEY')
        try:
            url = f'http://www.omdbapi.com/?apikey={api_key}&s={title}'
            response = requests.get(url)
            data = response.json()
            if data.get('Search'):
                search_results = data['Search']
        except:
            pass

    return render_template('edit_movie_search.html', user=user, movie=movie, search_results=search_results, title=title)


@app.route('/movie/<int:movie_id>')
def view_movie(movie_id):
    """Display a single movie's full details."""
    movie = data_manager.get_movie(movie_id)
    if not movie:
        abort(404)

    return render_template('view_movie.html', movie=movie)


@app.route('/users/<int:user_id>/confirm_edit_movie/<int:movie_id>/<imdb_id>', methods=['GET', 'POST'])
def confirm_edit_movie(user_id, movie_id, imdb_id):
    """Show updated OMDb data for a movie and allow confirmation of edit."""
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if not user or not movie or movie.user_id != user.id:
        abort(404)

    api_key = os.getenv('OMDB_API_KEY')
    url = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
    response = requests.get(url)
    data = response.json()

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director') or ''
        year = request.form.get('year') or ''
        rating = request.form.get('rating') or ''
        poster_url = request.form.get('poster_url')
        plot = request.form.get('plot')

        poster_url = poster_url if poster_url != 'N/A' else ''
        plot = plot if plot != 'N/A' else ''

        data_manager.update_movie(movie_id, title, director, year, rating, poster_url, plot)
        return redirect(url_for('user_movies', user_id=user.id))

    return render_template('confirm_edit_movie.html', user=user, movie=movie, new_data=data)


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete a user and all associated movies."""
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    data_manager.delete_user(user_id)
    return redirect(url_for('list_users'))


if __name__ == '__main__':
    app.run(debug=True)