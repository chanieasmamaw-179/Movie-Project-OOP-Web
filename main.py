import json
import logging
from movie import MovieCollection
from movie_storage import MovieStorage
from Movie_web_site_generator import Movie_web_site_generator


# Configure logging for the entire module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_data(file_path: str) -> dict:
    """Loads a JSON file.

    Args:
        file_path: The path to the JSON file.

    Returns:
        The contents of the JSON file as a dictionary, or an empty dictionary if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error: The file {file_path} is not a valid JSON.")
        return {}


def main():
    """Main function to handle command-line interactions for the movie collection."""
    # Ask for the API key to initialize MovieStorage
    api_key = ("afc2e88a").strip()
    storage = MovieStorage(api_key)
    movie_collection = MovieCollection(storage)

    while True:
        print("\nMenu")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Show statistics")
        print("6. Show random movie")
        print("7. Search movie by title")
        print("8. Show movies sorted by rating")
        print("9. Generate and save movie webpage")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "0":
                print("Exiting the program. Bye!")
                break

            elif choice == "1":
                movie_collection.list_movies()

            elif choice == "2":
                title = input("Enter movie title: ").strip()
                movie_collection.add_movie(title)

            elif choice == "3":
                title = input("Enter the title of the movie to delete: ").strip()
                movie_collection.delete_movie(title)

            elif choice == "4":
                title = input("Enter the title of the movie to update: ").strip()
                movie_collection.update_movie(title)

            elif choice == "5":
                movie_collection.show_stats()

            elif choice == "6":
                movie_collection.show_random_movie()

            elif choice == "7":
                title = input("Enter the title of the movie to search for: ").strip()
                movie_collection.search_movie(title)

            elif choice == "8":
                movie_collection.sort_movies_by_rating()

            elif choice == "9":
                movies = movie_collection.movies
                if not movies:
                    print("No movies available to generate a webpage.")
                else:
                    generator = Movie_web_site_generator(movies, 'movie_web.html')
                    generator.generate_html()
                    print("Webpage 'movie_web.html' has been generated and saved.")

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            logging.error(f"Value error: {e}. Please check your input and try again.")
        except KeyError as e:
            logging.error(f"Key error: {e}. It seems like a movie was not found.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
