from uuid import UUID
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse
from django_project.category_app.repository import DjangoORMCategoryRepository



# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:

        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        categories = [
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active,
            } for category in output.data
        ]
        return Response(status=HTTP_200_OK, data=categories)
    
    def retrieve(self, request: Request, pk=None):
        try:
            category_pk = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': 'Invalid category ID'})
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            result = use_case.execute(request=GetCategoryRequest(id=category_pk))
        except Exception as e:
            return Response(status=HTTP_404_NOT_FOUND, data={'error': str(e)})
        
        category_output = {
            'id': result.id,
            'name': result.name,
            'description': result.description,
            'is_active': result.is_active,
        }
        return Response(status=HTTP_200_OK, 
                        data=category_output,
                        )
                         