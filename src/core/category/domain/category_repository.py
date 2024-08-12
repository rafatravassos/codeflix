from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id):
        raise NotImplementedError    
    
    @abstractmethod
    def update(self, category):
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Category]:
        raise NotImplementedError