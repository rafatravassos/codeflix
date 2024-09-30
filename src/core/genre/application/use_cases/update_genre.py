from dataclasses import dataclass, field
from uuid import UUID
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class UpdateGenreRequest:
    id: UUID
    name: str
    category_ids: set[UUID] = field(default_factory=set)
    is_active: bool = None

class UpdateGenre:
    def __init__(self, repository: GenreRepository, category_repository):
        self.repository = repository
        self.category_repository = category_repository

    def execute(self, request: UpdateGenreRequest):
        category_ids = {category.id for category in self.category_repository.list()}
        if not request.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"The following categories do not exist: {request.category_ids - category_ids}")
        
        genre = self.repository.get_by_id(id=request.id)
        if genre is None:
            raise GenreNotFound(f"Genre with id {request.id} not found.")

        try:
            if request.is_active is True:
                genre.activate()
            elif request.is_active is False:
                genre.deactivate()

            genre.name = request.name
            genre.validate()
        except ValueError as error:
            raise InvalidGenre(error)
        
        genre.categories = request.category_ids

        self.repository.update(genre)