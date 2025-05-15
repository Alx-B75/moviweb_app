import requests
from flask import Flask, abort, render_template, redirect, url_for, request
from datamanager.sqlite_data_manager import SQLiteDataManager, db
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)


@app.route('/')
def home():
    return "<h1>Welcome to MoviWeb App</h1>"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            data_manager.add_user(name)
            return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director') or ''
        year = request.form.get('year') or ''
        rating = request.form.get('rating') or ''

        if title:
            try:
                api_key = os.getenv('OMDB_API_KEY')
                url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
                response = requests.get(url)
                data = response.json()
                director = data.get('Director') or director
                year = data.get('Year') or year
                rating = data.get('imdbRating') or rating
            except:
                pass

            data_manager.add_movie(user_id, title, director, year, rating)
            return redirect(url_for('user_movies', user_id=user.id))

    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(user_id, movie_id):
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if not user or not movie or movie.user_id != user.id:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director') or ''
        year = request.form.get('year') or ''
        rating = request.form.get('rating') or ''

        if title:
            try:
                api_key = os.getenv('OMDB_API_KEY')
                url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
                response = requests.get(url)
                data = response.json()
                director = data.get('Director') or director
                year = data.get('Year') or year
                rating = data.get('imdbRating') or rating
                print(f"OMDb raw response: {data}")
            except:
                pass

            data_manager.update_movie(movie_id, title, director, year, rating)
            return redirect(url_for('user_movies', user_id=user.id))

    return render_template('edit_movie.html', user=user, movie=movie)



@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if not user or not movie or movie.user_id != user.id:
        abort(404)

    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user.id))


if __name__ == '__main__':
    app.run(debug=True)
