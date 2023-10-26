# apps/orders/views.py

import json
from .data_validators import OrderValidator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status

class OrderViewset(viewsets.ViewSet):

    def list(self, request):
        return Response({"message": "Listing order"})

    def create(self, request):
        """
        Create order from user input
        """
        try:
            validated_data = OrderValidator(**self.request.data)
        except ValueError as error:
            error_message = json.loads(error.json())[0]
            error_message.pop('url', None)
            error_message.pop('ctx', None)
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass