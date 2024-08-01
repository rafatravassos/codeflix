from unittest.mock import MagicMock, create_autospec
from uuid import UUID
import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.application.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.category_repository import CategoryRepository


class TestGetCategory:
    def test_create_category_with_valid_data(self):
        category = Category(
            name="Filme", 
            description="Descrição do filme", 
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(
            id=uuid.uuid4()
            )
        
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,)

