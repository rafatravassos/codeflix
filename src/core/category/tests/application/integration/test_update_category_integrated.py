from unittest.mock import create_autospec
import uuid

from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    ## TODO: Criar para categoria inexistente
    ## TODO: Criar testes de ativação com descrição
    ## TODO: Criar testes de desativação com descrição
    ## TODO: Criar testes para verificação de erros de validação
    def test_can_update_category_name_and_description(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository = create_autospec(InMemoryCategoryRepository)
        repository.get_by_id.return_value = category

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
