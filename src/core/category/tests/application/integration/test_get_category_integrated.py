from uuid import UUID
import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.application.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.exceptions import CategoryNotFound


class TestCreateCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            name = "filme" ,
            description = "Descrição do filme")
        
        category_serie = Category(
            name = "serie" ,
            description = "Descrição da serie")

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id = category_filme.id)
        
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id = category_filme.id,
            name = category_filme.name,
            description = category_filme.description,
            is_active = category_filme.is_active,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_filme = Category(
            name = "filme" ,
            description = "Descrição do filme")
        
        category_serie = Category(
            name = "serie" ,
            description = "Descrição da serie")

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        
        request = GetCategoryRequest(
            id = not_found_id
            )
        
        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

