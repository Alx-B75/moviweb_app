from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """Abstract base class defining the contract for a data manager."""

    @abstractmethod
    def get_all_users(self):
        """Return a list of all users."""
        pass

    @abstractmethod
    def get_user(self, user_id):
        """Return a single user by ID."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return all movies belonging to a user."""
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        """Return a single movie by ID."""
        pass

    @abstractmethod
    def add_user(self, name):
        """Add a new user with the given name."""
        pass

    @abstractmethod
    def add_movie(self, user_id, title, director, year, rating):
        """Add a new movie to the given user."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, title=None, director=None, year=None, rating=None):
        """Update an existing movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        pass