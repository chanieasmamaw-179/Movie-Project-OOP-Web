import csv
from storage_interface import StorageInterface

class CSVStorage(StorageInterface):
    DATA_FILE = 'movies.csv'

    def get_movies(self):
        """Load movies from the CSV file."""
        movies = {}
        try:
            with open(self.DATA_FILE, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title_lower = row['title'].lower()
                    movies[title_lower] = row
        except FileNotFoundError:
            print("CSV file not found.")
        return movies

    def save_movies(self, movies):
        """Save movies to the CSV file."""
        with open(self.DATA_FILE, mode='w', newline='') as file:
            fieldnames = ['title', 'rating', 'year']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for movie in movies.values():
                writer.writerow(movie)
