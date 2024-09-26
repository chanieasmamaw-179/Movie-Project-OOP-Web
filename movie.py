from storage_interface import StorageInterface
from fuzzywuzzy import process
import random
import statistics as stat
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)


class MovieCollection:
    """Class to manage a collection of movies."""

    def __init__(self, storage: StorageInterface):
        """Initialize the movie collection with a storage interface."""
        self.storage = storage
        self.movies = self.storage.get_movies()  # Load movies from storage

    def fetch_movie_data(self, movie_title: str) -> Optional[Dict]:
        """Fetch movie data from an external API or local storage."""
        movie = self.movies.get(movie_title.lower())
        if not movie:
            movie = self.storage.fetch_movie_info(movie_title)
            if not movie:
                logging.warning(f"Movie '{movie_title}' not found in the API.")
                return None
        return movie

    def add_movie(self, title: str):
        """Add a new movie to the collection."""
        movie_data = self.fetch_movie_data(title)
        if movie_data:
            self.movies[title.lower()] = movie_data
            self.storage.save_movies(self.movies)  # Save the updated collection
            logging.info(f"Movie '{title}' added successfully.")
        else:
            logging.warning(f"Movie '{title}' not found.")

    def delete_movie(self, title: str):
        """Delete a movie from the collection."""
        title_lower = title.lower()
        if title_lower in self.movies:
            del self.movies[title_lower]
            self.storage.save_movies(self.movies)
            logging.info(f"Movie '{title}' deleted successfully.")
        else:
            match, score = process.extractOne(title_lower, self.movies.keys())
            if score >= 80:
                logging.info(f"Movie '{title}' not found. Did you mean '{match}'?")
            else:
                logging.warning(f"Movie '{title}' not found in the collection.")

    def update_movie(self, title: str):
        """Update an existing movie in the collection."""
        title_lower = title.lower()
        if title_lower in self.movies:
            movie_data = self.fetch_movie_data(title)
            if movie_data:
                self.movies[title_lower] = movie_data
                self.storage.save_movies(self.movies)
                logging.info(f"Movie '{title}' updated successfully.")
            else:
                logging.warning(f"Movie '{title}' not found in the API.")
        else:
            match, score = process.extractOne(title_lower, self.movies.keys())
            if score >= 80:
                logging.info(f"Movie '{title}' not found. Did you mean '{match}'?")
            else:
                logging.warning(f"Movie '{title}' not found in the collection.")

    def list_movies(self):
        """List all movies in the collection."""
        if not self.movies:
            logging.info("No movies available.")
        else:
            for title, data in self.movies.items():
                logging.info(f"{title.title()} - Rating: {data.get('rating', 'N/A')}")

    def show_stats(self):
        """Show movie statistics."""
        if not self.movies:
            logging.info("No movies available to show statistics.")
            return

        ratings = []
        for movie in self.movies.values():
            try:
                if 'rating' in movie and movie['rating'] is not None:
                    ratings.append(float(movie['rating']))
            except ValueError:
                logging.warning(f"Invalid rating found for movie: {movie.get('title', 'Unknown')}")

        if ratings:
            logging.info(f"Average Rating: {stat.mean(ratings):.2f}")
            logging.info(f"Highest Rating: {max(ratings):.2f}")
            logging.info(f"Lowest Rating: {min(ratings):.2f}")
        else:
            logging.info("No valid ratings available.")

    def show_random_movie(self):
        """Show a random movie from the collection."""
        if self.movies:
            random_movie = random.choice(list(self.movies.values()))
            logging.info(f"Random Movie: {random_movie['title']} (Rating: {random_movie.get('rating', 'N/A')})")
        else:
            logging.info("No movies available.")

    def search_movie(self, title: str):
        """Search for a movie by title using fuzzy matching."""
        titles = list(self.movies.keys())
        match, score = process.extractOne(title.lower(), titles)
        if score >= 80:
            movie = self.movies[match]
            logging.info(f"Movie Found: {movie['title']} (Rating: {movie.get('rating', 'N/A')})")
        else:
            logging.warning(f"No match found for '{title}'.")

    def sort_movies_by_rating(self):
        """Sort movies by their rating and display them."""
        sorted_movies = sorted(self.movies.items(), key=lambda x: float(x[1].get('rating', 0)), reverse=True)
        for title, movie in sorted_movies:
            logging.info(f"{movie['title']} - Rating: {movie.get('rating', 'N/A')}")
