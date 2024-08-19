from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategory, InvalidCategoryData
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_update_category_with_provided_fields(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category=category)  # Usando o próprio repositório pra salvar
        use_case = UpdateCategory(repository=repository)

        request = UpdateCategoryRequest(
            id=category.id,
            name="Séries",
            description="Séries de filmes",
            is_active=False,
        )
        response = use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert response is None
        assert updated_category.name == "Séries"
        assert updated_category.description == "Séries de filmes"
        assert updated_category.is_active is False

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

        with pytest.raises(InvalidCategory) as exc:
            response = use_case.execute(request)
