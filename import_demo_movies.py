import os
import requests
from flask import Flask
from dotenv import load_dotenv
from datamanager.sqlite_data_manager import SQLiteDataManager

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)

with app.app_context():
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

    # Check if user already exists
    existing = [u for u in data_manager.get_all_users() if u.name == "Best 100 Movies"]
    if existing:
        user = existing[0]
        user_id = user.id
    else:
        user = data_manager.add_user("Best 100 Movies")
        user_id = user.id if hasattr(user, 'id') else data_manager.get_all_users()[-1].id

    top_movies = ['The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'The Godfather Part II', '12 Angry Men', "Schindler's List", 'The Lord of the Rings: The Return of the King', 'Pulp Fiction', 'The Good, the Bad and the Ugly', 'The Lord of the Rings: The Fellowship of the Ring', 'Fight Club', 'Forrest Gump', 'Inception', 'The Empire Strikes Back', 'The Lord of the Rings: The Two Towers', "One Flew Over the Cuckoo's Nest", 'Goodfellas', 'The Matrix', 'Seven Samurai', 'Star Wars', 'Se7en', "It's a Wonderful Life", 'The Silence of the Lambs', 'Saving Private Ryan', 'City of God', 'Interstellar', 'Life Is Beautiful', 'The Green Mile', 'Terminator 2: Judgment Day', 'Back to the Future', 'Spirited Away', 'Psycho', 'Parasite', 'Léon: The Professional', 'The Pianist', 'The Lion King', 'Gladiator', 'American History X', 'The Departed', 'Whiplash', 'The Prestige', 'Casablanca', 'Grave of the Fireflies', 'The Intouchables', 'Modern Times', 'City Lights', 'Once Upon a Time in the West', 'Rear Window', 'Alien', 'Apocalypse Now', 'Memento', 'Raiders of the Lost Ark', 'The Great Dictator', 'Django Unchained', 'WALL·E', 'The Lives of Others', 'Sunset Blvd.', 'Paths of Glory', 'The Shining', 'Avengers: Infinity War', 'Witness for the Prosecution', 'Aliens', 'American Beauty', 'Dr. Strangelove', 'Spider-Man: Into the Spider-Verse', 'Oldboy', 'Coco', 'Braveheart', 'Das Boot', 'Toy Story', 'Amadeus', 'Inglourious Basterds', '3 Idiots', 'Princess Mononoke', 'Your Name', 'Avengers: Endgame', 'Capernaum', 'High and Low', 'Good Will Hunting', 'Requiem for a Dream', 'Come and See', '2001: A Space Odyssey', 'Eternal Sunshine of the Spotless Mind', 'Reservoir Dogs', 'Tumbbad', "Singin' in the Rain", 'Like Stars on Earth', 'Toy Story 3', 'Lawrence of Arabia', 'Citizen Kane', 'North by Northwest', 'Vertigo', 'Double Indemnity', 'Full Metal Jacket', 'A Clockwork Orange', 'Bicycle Thieves', 'The Hunt', 'The Kid', 'The Father']

    for title in top_movies:
        try:
            url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
            response = requests.get(url)
            data = response.json()

            if data.get("Response") == "True":
                movie_title = data.get("Title")
                director = data.get("Director")
                year = data.get("Year")
                rating = data.get("imdbRating")
                poster_url = data.get("Poster") if data.get("Poster") != "N/A" else ""
                plot = data.get("Plot") if data.get("Plot") != "N/A" else ""

                data_manager.add_movie(user_id, movie_title, director, year, rating, poster_url, plot)
                print(f"✅ Added: {movie_title}")
            else:
                print(f"❌ Not found: {title}")

        except Exception as e:
            print(f"⚠️ Error adding {title}: {e}")