import json
import requests
import csv
import logging
from storage_interface import StorageInterface

class MovieStorage(StorageInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.json_file_path = 'movies.json'
        self.csv_file_path = 'movies.csv'

    def get_movies(self):
        """Load movies from a JSON file."""
        self.file_path = 'movies.json'
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("Movies file not found. Starting with an empty collection.")
            self.save_movies({})  # Create a new empty JSON file
            return {}
        except json.JSONDecodeError:
            logging.error("Error reading movies file. Starting with an empty collection.")
            return {}

    def save_movies(self, movies):
        """Save movies to both JSON and CSV files."""
        self.save_movies_json(movies)
        self.save_movies_csv(movies)

    def save_movies_json(self, movies):
        """Save movies to a JSON file."""
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            json.dump(movies, file, ensure_ascii=False, indent=4)
            logging.info("Movies saved to JSON file successfully.")

    def save_movies_csv(self, movies):
        """Save movies to a CSV file."""
        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['title', 'year', 'rating', 'actors', 'poster']  # Add any additional fields you need
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for title, movie in movies.items():
                    writer.writerow({
                        'title': title,
                        'year': movie.get('Year', ''),
                        'rating': movie.get('Rated', ''),
                        'actors': movie.get('Actors', ''),
                        'poster': movie.get('Poster', '')
                    })
            logging.info("Movies saved to CSV file successfully.")
        except Exception as e:
            logging.error(f"Error saving movies to CSV: {e}")

    def fetch_movie_info(self, title: str):
        """Fetch movie information from an external API."""
        url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('Response') == "True":
                return data
            else:
                logging.warning(f"API response for '{title}': {data.get('Error')}")
                return None
        except requests.RequestException as e:
            logging.error(f"Error fetching movie info: {e}")
            return None
