import pytest
from uuid import UUID
import uuid
from src.core.genre.domain.genre import Genre

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()
    
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            Genre("a" * 256)

    def test_name_must_not_be_empty_string(self):
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            Genre("")

    def test_create_genre_with_default_values(self):
        genre = Genre("Documentary")
        assert genre.name == "Documentary"
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_create_genre_with_custom_values(self):
        gen_id = uuid.uuid4()
        genre = Genre("Classical", id=gen_id, is_active=False)
        assert genre.id == gen_id
        assert genre.name == "Classical"
        assert genre.is_active is False

    def test_genre_print(self):
        gen_id = uuid.uuid4()
        genre = Genre("Classical", id=gen_id, is_active=False)
        expected_output = f"Genre(\n\tid={gen_id},\n\tname=Classical,\n\tis_active=False\n)"
        assert str(genre) == expected_output

    
class TestActivateGenre:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name = "Action",
             is_active=False
             )
        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre("Drama",  is_active=True)
        genre.activate()

        assert genre.is_active is True

class TestDeactivateGenre:
    def test_deactivate_active_genre(self):
        genre = Genre("Anime", is_active=True)
        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre("Filme", is_active=False)
        genre.deactivate()

        assert genre.is_active is False

class TestChangeName:
    def test_change_name(self):
        genre = Genre("Action")
        genre.change_name("Action Movie")

        assert genre.name == "Action Movie"

    def test_when_name_is_empty(self):
        genre = Genre("Action")
        with pytest.raises(ValueError, match="name cannot be an empty string"):
            genre.change_name("")


class TestAddCategory:
    def test_add_category_to_genre(self):
        gen_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre = Genre("Classical", id=gen_id, is_active=False)
        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories

    def test_add_multiple_categories(self):
        genre = Genre("Romance")
        category_id1 = uuid.uuid4()
        category_id2 = uuid.uuid4()
        genre.add_category(category_id1)
        genre.add_category(category_id2)
        assert category_id1 in genre.categories
        assert category_id2 in genre.categories
        assert genre.categories == {
            category_id1,
            category_id2,
        }
        
class TestRemoveCategory:
    def test_remove_category_from_genre(self):
        gen_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre = Genre("Classical", id=gen_id, is_active=False)
        genre.add_category(category_id)
        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories

# class TestEquality:
#     def test_when_categories_have_same_id_they_area_equals(self):
#         common_id = uuid.uuid4()
#         category1 = Category("Filme", id=common_id)
#         category2 = Category("Filme", id=common_id)

#         assert category1 == category2

#     def test_equality_different_classes(self):
#         class Dummy:
#             pass

#         common_id = uuid.uuid4()
#         category = Category("Filme", id=common_id)
#         dummy = Dummy()
#         dummy.id = common_id

#         assert category != dummy
