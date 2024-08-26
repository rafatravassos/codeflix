import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreatedAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        #create a new category
        create_response = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )

        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        #Check if category exists
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        #check category update
        update_request = api_client.put(f"/api/categories/{created_category_id}/",
                                        data = {
                                            "name": "Updated Movie",
                                            "description": "Updated movie description",
                                            "is_active": True,
                                        }
                                        )
        assert update_request.status_code == 204

        #check updated category
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Updated Movie",
                    "description": "Updated movie description",
                    "is_active": True,
                }
            ]
        }

        #check deleted category
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/")
        assert delete_response.status_code == 204

        #check if category deleted
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}