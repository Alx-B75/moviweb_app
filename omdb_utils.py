import os
import requests

def fetch_omdb_data(title):
    """Try to fetch full movie details using fuzzy search and fallback to IMDb ID."""
    api_key = os.getenv('OMDB_API_KEY')

    if not api_key or not title:
        return {}

    try:
        search_url = f'http://www.omdbapi.com/?apikey={api_key}&s={title}'
        search_response = requests.get(search_url).json()
        results = search_response.get('Search')

        if results and len(results) > 0:
            imdb_id = results[0].get('imdbID')
            detail_url = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
            detail_response = requests.get(detail_url).json()
            return detail_response
    except:
        pass

    return {}
