from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

    
@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository=create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository



class TestUpdateGenre:
    def test_update_genre_with_invalid_id(self, mock_genre_repository, mock_empty_category_repository):
        mock_genre_repository.get_by_id.return_value = None
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )

        with pytest.raises(GenreNotFound, match="Genre with .* not found") as exc:
            use_case.execute(request=UpdateGenreRequest(
                id=uuid.uuid4(),
                name="Documentary"
            ))
        
    def test_update_genre_with_valid_input(self, mock_genre_repository, mock_empty_category_repository):
        mock_genre = Genre(
            id=uuid.uuid4(),
            name="Action",
            is_active=True
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = mock_genre
        use_case = UpdateGenre(repository = mock_repository, category_repository=mock_empty_category_repository)
        request = UpdateGenreRequest(
            id=mock_genre.id,
            name="Documentary"
        )
        response = use_case.execute(request)
        assert mock_genre.name == "Documentary"

    def test_update_genre_with_invalid_value(self, mock_genre_repository, mock_empty_category_repository):
        mock_genre = Genre(
            id=uuid.uuid4(),
            name="Action",
            is_active=True
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = mock_genre
        use_case = UpdateGenre(
            repository = mock_repository,
            category_repository=mock_empty_category_repository)
        request = UpdateGenreRequest(
            id=mock_genre.id,
            name=""
        )
        with pytest.raises(InvalidGenre, match="name cannot be an empty string") as exc:
            use_case.execute(request)

    def test_update_genre_with_invalid_categories(self, mock_genre_repository, mock_empty_category_repository):
        mock_genre = Genre(
            id=uuid.uuid4(),
            name="Action",
            is_active=True
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = mock_genre
        use_case = UpdateGenre(
            repository = mock_repository,
            category_repository=mock_empty_category_repository)
        category_id = uuid.uuid4()
        request = UpdateGenreRequest(
            id=mock_genre.id,
            name="Documentary",
            category_ids={category_id}
        )
        with pytest.raises(RelatedCategoriesNotFound) as exc:
            use_case.execute(request)

    def test_update_genre_with_valid_categories(
            self, 
            mock_genre_repository,         
            movie_category,
            documentary_category,
            mock_category_repository_with_categories):
        mock_genre = Genre(
            id=uuid.uuid4(),
            name="Action",
            is_active=True,
            categories={movie_category.id}
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = mock_genre

        use_case = UpdateGenre(
            repository = mock_repository,
            category_repository=mock_category_repository_with_categories)

        request = UpdateGenreRequest(
            id=mock_genre.id,
            name="Documentary",
            category_ids={documentary_category.id}
        )

        output = use_case.execute(request)
        assert mock_genre.name == "Documentary"
        assert mock_genre.categories == {documentary_category.id}
