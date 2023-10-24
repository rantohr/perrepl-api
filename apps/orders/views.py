# apps/orders/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response

class OrderViewset(viewsets.ViewSet):

    def list(self, request):
        return Response({"message": "Listing order"})

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass