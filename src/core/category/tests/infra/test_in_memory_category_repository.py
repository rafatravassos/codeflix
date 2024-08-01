from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category("Filme", description="Series em geral")
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category("Filme", description="Series em geral")
        repository.save(category)

        category_found = repository.get_by_id(category.id)

        assert repository.categories[0] == category
        assert repository.categories[0].id == category.id
