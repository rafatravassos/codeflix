import pytest
from uuid import UUID
import uuid
from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()
    
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            Category("a" * 256)

    def test_name_must_not_be_empty_string(self):
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            Category("")

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category("Filme")
        assert isinstance(category.id, UUID)

    def test_create_category_with_default_values(self):
        category = Category("Filme")
        assert category.name == "Filme"
        assert category.description == ""
        assert category.is_active is True

    def test_create_category_with_custom_values(self):
        cat_id = uuid.uuid4()
        category = Category("Jogo", id=cat_id, description="Um jogo de ação", is_active=False)
        assert category.id == cat_id
        assert category.name == "Jogo"
        assert category.description == "Um jogo de ação"
        assert category.is_active is False

    def test_category_print(self):
        cat_id = uuid.uuid4()
        category = Category("Filme", id=cat_id, description="Categoria de filme", is_active=True)
        expected_output = f"Category(\n\tid={cat_id},\n\tname=Filme,\n\tdescription=Categoria de filme,\n\tis_active=True\n)"
        assert str(category) == expected_output

    def test_category_repr(self):
        cat_id = uuid.uuid4()
        category = Category("Jogo", id=cat_id, description="Um jogo de ação", is_active=False)
        expected_output = f"<Category Jogo ({cat_id})>"
        assert repr(category) == expected_output
    
class TestUpdateCategory:
    def test_category_update_with_name_and_description(self):
        category = Category("Filme", description="Categoria de filme")
        category.update_category(name="Serie", description="Serie em geral")

        assert category.name == "Serie"
        assert category.description == "Serie em geral"

    def test_category_update_with_name_exceeding_255_characters(self):
        category = Category("Filme", description="Series em geral")
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            category.update_category(name="a" * 256, description="Series em geral")

    def test_category_update_with_empty_name(self):
        category = Category("Filme", description="Series em geral")
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            category.update_category(name="", description="Series em geral")

class TestActivateCategory:
    def test_activate_inactive_category(self):
        category = Category("Filme", description="Series em geral", is_active=False)
        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category("Filme", description="Series em geral", is_active=True)
        category.activate()

        assert category.is_active is True

class TestDeactivateCategory:
    def test_deactivate_active_category(self):
        category = Category("Filme", description="Series em geral", is_active=True)
        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category("Filme", description="Series em geral", is_active=False)
        category.deactivate()

        assert category.is_active is False

class TestEquality:
    def test_when_categories_have_same_id_they_area_equals(self):
        common_id = uuid.uuid4()
        category1 = Category("Filme", id=common_id)
        category2 = Category("Filme", id=common_id)

        assert category1 == category2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category("Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
