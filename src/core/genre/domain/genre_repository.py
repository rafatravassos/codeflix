from abc import ABC, abstractmethod

from src.core.genre.domain import genre
from src.core.genre.domain.genre import Genre


class GenreRepository(ABC):
    @abstractmethod
    def save(self, genre):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id):
        raise NotImplementedError    
    
    @abstractmethod
    def update(self, genre):
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Genre]:
        raise NotImplementedError