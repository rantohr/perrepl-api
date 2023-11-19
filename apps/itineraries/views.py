from typing import List, Dict

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from django.db import transaction
from django.apps import apps

from .models import Itinerary, ItinerarySegment
from .data_validator import ItineraryValidator
from .cotation_datasets import CotationDataset
from .serializers import ItinerarySerializer

from api_config import mixins
from apps.mada_countries.models import MadaCountry

class ItineraryViewSet(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    GenericViewSet
):
    queryset = Itinerary.objects.all()

    def get_serializer_class(self):
        return ItinerarySerializer
    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = self.get_serializer(qs, many=True)

        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)

    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(ItineraryValidator)
        if not isinstance(validated_data_obj, ItineraryValidator):
            return Response(validated_data_obj, status=status.HTTP_400_BAD_REQUEST)
        
        validated_json_data = validated_data_obj.model_dump()
        segments = validated_json_data.pop("segments")
        with transaction.atomic():
            itinerary = Itinerary(user=self.request.user, **validated_json_data)
            itinerary.save()

            for segment in segments:
                origin_obj = self._get_location(segment, "start_location")
                destination_obj = self._get_location(segment, "end_location")
                cotations = self._get_cotation_object(segment)

                itinerary_segment = ItinerarySegment(
                    user=self.request.user,
                    start_location=origin_obj,
                    end_location=destination_obj,
                    **segment
                )
                itinerary_segment.save()
                
                self._add_cotation(itinerary_segment, cotations)
                itinerary.segments.add(itinerary_segment)

        serializer = ItinerarySerializer(itinerary)
        return Response({"Status": "COMPLETED", "OrderData": serializer.data}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None, *args, **kwargs):
        itinerary_data = request.data
        itinerary = self.get_object()
        segments = itinerary_data.pop("segments", None)
        if segments is not None:
            for segment in segments:
                self.update_m2m_field(ItinerarySegment, itinerary, "segments", segment)
        
        self.update_without_relation(itinerary, itinerary_data)
        return Response(self.get_serializer(itinerary).data)
    
    def update_without_relation(self, instance, data):
        if data:
            for key, value in data.items():
                setattr(instance, key, value)

    def update_m2m_field(self, model, itinerary, field_name, segment):
        itinerary_segment = model.objects.get(id=segment["id"])

        origin_obj = self._get_location(segment, "start_location")
        destination_obj = self._get_location(segment, "end_location")
        if origin_obj is not None:
            itinerary_segment.start_location = origin_obj
            itinerary_segment.save()
        if destination_obj is not None:
            itinerary_segment.end_location = destination_obj
        itinerary_segment.save()

        new_cotations = self._get_cotation_object(segment)
        for k, v in new_cotations.items():
            if len(v)!=0:
                cotations = getattr(itinerary_segment, k)
                cotations.clear()
                for cotation in v:
                    cotations.add(cotation)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _add_cotation(self, segment: ItinerarySegment, cotations: dict):
        """
        Summary: Add dynamically cotation (hotel, activity, etc) to the segment
        Args:
            - cotations (Dict[app_name, List[object]]]) -> example: {'hotels': [hotel1, hotel2], 'activities': [activity1, activity2]}
            - segment (ItinerarySegment): The segment is an instance saved of ItinerarySegment
        """

        for k, v in cotations.items():
            if len(v)!=0:
                for cotation in v:
                    obj = getattr(segment, k)
                    obj.add(cotation)
        
    @staticmethod
    def _get_cotation_object(segment: dict) -> Dict[str, List]:
        dataset = CotationDataset().to_dict()
        output = dict((k, list()) for k, v in dataset.items())
        for k, v in dataset.items():
            cotations = segment.pop(k, None)
            if cotations is not None:
                model = apps.get_model(app_label=k, model_name=v)
                for cotation in cotations:
                    index = cotation.get("id")
                    obj =  model.objects.get(id=index)
                    output[k].append(obj)
        return output
    
    @staticmethod
    def _get_location(segment, pos):
        index = segment.pop(pos)
        if index is not None:
            return MadaCountry.objects.get(id=index)
        return None
