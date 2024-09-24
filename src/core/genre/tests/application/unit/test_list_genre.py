from unittest.mock import create_autospec

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
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

class TestListGenre:
    def test_when_no_genres_in_repository_then_return_empty_list(self):
        genre = Genre(
            name="Drama", 
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = []

        use_case = ListGenre(repository=mock_repository)
        
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0

    def test_when_genres_in_repository_then_return_list(self):
        genre_drama = Genre(
            name="Drama", 
        )
        genre_comedia = Genre(
            name="Comédia", 
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = [
            genre_drama, 
            genre_comedia,  # Added a second genre to test list
        ]

        use_case = ListGenre(repository=mock_repository)
        
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 2

    def test_list_genres_with_associated_categories(
            self,
            documentary_category,
            movie_category
        ):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = [
            Genre(
                name="Drama",
                categories={documentary_category.id, movie_category.id},
            )
        ]
        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())
        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_repository.list.return_value[0].id,
                    name=genre_repository.list.return_value[0].name,
                    is_active=True,
                    categories={documentary_category.id, movie_category.id}
                )
            ])
        
        


    