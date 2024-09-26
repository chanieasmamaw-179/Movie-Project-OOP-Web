from abc import ABC, abstractmethod
from typing import Dict

class StorageInterface(ABC):
    @abstractmethod
    def get_movies(self) -> Dict[str, dict]:
        """Load movies from storage.

        Returns:
            A dictionary where keys are movie titles and values are dictionaries containing movie details.
        """
        pass

    @abstractmethod
    def save_movies(self, movies: Dict[str, dict]):
        """Save movies to storage.

        Args:
            movies: A dictionary where keys are movie titles and values are dictionaries containing movie details.
        """
        pass
