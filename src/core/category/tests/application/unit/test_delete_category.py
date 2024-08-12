from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filme", 
            description="Descrição do filme", 
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        assert mock_repository.get_by_id(category.id) is not None

        use_case = DeleteCategory(mock_repository)

        request = DeleteCategoryRequest(id=category.id)
        use_case.execute(request)

        mock_repository.delete.assert_called_once_with(category.id)

      
    def test_when_category_exists_then_return_response_dto(self):
        mock_category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=mock_category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=mock_category.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )      



    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=mock_repository)
        
        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(DeleteCategoryRequest(id=uuid.uuid4()))

        mock_repository.delete.assert_not_called()

        