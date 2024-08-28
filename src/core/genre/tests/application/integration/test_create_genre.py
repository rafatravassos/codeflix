from unittest.mock import create_autospec
import uuid
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain.genre_repository import GenreRepository


import pytest

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



class TestCreateGenre:

    def test_create_genre_with_associated_categories(
            self,
            movie_category: Category,
            documentary_category: Category,
            category_repository: InMemoryCategoryRepository,
            ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        use_case = CreateGenre(
            genre_repository = genre_repository, 
            category_repository = category_repository, 
            )
        
        input = CreateGenre.Input(
            name="Action", 
            category_ids={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)
        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active == True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        mock_empty_category_repository: CategoryRepository
    ):
        
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            genre_repository = genre_repository, 
            category_repository = mock_empty_category_repository, 
            )
        
        category_id=uuid.uuid4()
        input = CreateGenre.Input(
            name="Action", 
            category_ids={category_id}, 
        )
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        assert str(category_id) in str(exc_info.value)

    def teste_create_genre_without_categories(
        self,
    ):
        ...



