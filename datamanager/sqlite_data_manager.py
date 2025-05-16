from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

db = SQLAlchemy()

class User(db.Model):
    """User model representing an app user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', backref='user', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"

class Movie(db.Model):
    """Movie model representing a user's favorite movie."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    poster_url = db.Column(db.String(300))
    plot = db.Column(db.Text)

    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"

class SQLiteDataManager(DataManagerInterface):
    """SQLite-based implementation of the DataManagerInterface."""

    def __init__(self, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def add_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def add_movie(self, user_id, title, director, year, rating, poster_url, plot):
        new_movie = Movie(
            title=title,
            director=director,
            year=year,
            rating=rating,
            user_id=user_id,
            poster_url=poster_url,
            plot=plot
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, title=None, director=None, year=None, rating=None, poster_url=None, plot=None):
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        if title is not None:
            movie.title = title
        if director is not None:
            movie.director = director
        if year is not None:
            movie.year = year
        if rating is not None:
            movie.rating = rating
        db.session.commit()
        return True

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        db.session.delete(movie)
        db.session.commit()
        return True

    def delete_user(self, user_id):
        """Delete a user and all their associated movies."""
        user = User.query.get(user_id)
        if user:
            Movie.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            return True
        return False
