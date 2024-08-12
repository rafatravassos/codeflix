import pytest
from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Series",
            description="General series category",
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active

    def test_update_category_in_database(self):
        category = Category(
            name="Series",
            description="General series category",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category)

        category.name = "Series updated"
        category.description = "Updated general series category"
        repository.update(category)

        category_db = CategoryModel.objects.get(id=category.id)
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active


    def test_delete_category_in_database(self):
        category = Category(
            name="Series",
            description="General series category",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category)
        assert CategoryModel.objects.count() == 1
        repository.delete(category.id)

        assert CategoryModel.objects.count() == 0