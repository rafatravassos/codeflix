from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category: Category, documentary_category: Category):
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository=create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository
class TestUpdateGenre:
    def test_update_genre_with_valid_ids(
            self,
            movie_category: Category,
            documentary_category: Category,
            category_repository: InMemoryCategoryRepository,
        ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre = Genre(
            id=uuid.uuid4(),
            name="Drama",
            categories={documentary_category.id},
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, 
            category_repository=category_repository, 
        )

        request = UpdateGenreRequest(
            id=genre.id,
            name="Romance",
            category_ids={movie_category.id},
        )

        output = use_case.execute(request)
        saved_genre = genre_repository.get_by_id(genre.id)
        assert saved_genre.id == genre.id
        assert saved_genre.name == "Romance"
        assert saved_genre.categories == {movie_category.id}
