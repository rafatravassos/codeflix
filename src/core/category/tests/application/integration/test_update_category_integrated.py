from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)


        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
            description = "Categoria Série"
        )

        response = use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == "Série"
        assert updated_category.description == "Categoria Série"
    
    def test_update_category_not_found(self):

        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)


        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=uuid.uuid4(), 
            name="Série",
            description = "Categoria Série"
        )

        with pytest.raises(CategoryNotFound) as exc:
            response = use_case.execute(request)

    def test_update_category_with_invalid_data(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)


        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="",
            description = ""
        )

        with pytest.raises(InvalidCategoryData) as exc:
            response = use_case.execute(request)
