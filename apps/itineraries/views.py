import typing
from typing import List, Dict

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.decorators import action

from django.db import transaction
from django.apps import apps

from .models import Itinerary, ItinerarySegment
from .data_validator import ItineraryValidator, ItinerarySegmentValidator
from .cotation_datasets import CotationDataset
from .serializers import ItinerarySerializer

from api_config import mixins
from apps.mada_countries.models import MadaCountry
from apps.travelers.models import Traveler
from apps.orders.models import Order
from apps.exceptions import (
    MissingClienOROrder
)

class ItineraryViewSet(
    mixins.ValidatorMixin,
    mixins.UserQuerySetMixin,
    mixins.PermissionMixin,
    GenericViewSet
):
    queryset = Itinerary.objects.all()

    def get_serializer_class(self):
        return ItinerarySerializer
    
    def paginate_and_response(self, serializer):
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(page)
        return self.get_paginated_response([])
    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = self.get_serializer(qs, many=True)
        return self.paginate_and_response(serializer)
    
    def create(self, request, *args, **kwargs):
        validated_data_obj = self._validate_data(ItineraryValidator)
        if not isinstance(validated_data_obj, ItineraryValidator):
            return Response(validated_data_obj, status=status.HTTP_400_BAD_REQUEST)
        
        validated_json_data = validated_data_obj.model_dump()
        segments = validated_json_data.pop("segments")
        c_id = validated_json_data.pop("client", None)
        o_id = validated_json_data.pop("order", None)
        try:
            serializer = self.create_and_save_itinerary(validated_json_data, segments, client_id=c_id, order_id=o_id)
            return Response({"Status": "COMPLETED", "Itinerary": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errorMessage": str(e.detail)}, status=e.status_code)

    def create_and_save_itinerary(self, basic_info_data: Dict, segments: List, client_id: List=None, order_id: List=None):
        c_id, o_id = None, None
        if client_id and client_id is not None:    
            c_id = client_id[0].get("id")
        if order_id and order_id is not None:
            o_id = order_id[0].get("id")
            
        with transaction.atomic():
            client, order = None, None
            if c_id:
                try:
                    client = Traveler.objects.get(id=c_id)
                except Traveler.DoesNotExist:
                    raise MissingClienOROrder(detail="Give client doesn't exit ")
            
            if o_id:
                order = client.orders_created.filter(id=o_id).first()# Order.objects.get(id=o_id)
                if order is None:
                    raise MissingClienOROrder(detail="Selected order doesn't belong to the user")

            itinerary = Itinerary(user=self.request.user, client=client, order=order ,**basic_info_data)
            itinerary.save()

            for segment in segments:
                origin_obj = self._get_location(segment, "start_location")
                destination_obj = self._get_location(segment, "end_location")
                cotations = self._get_cotation_object(segment)
                if isinstance(cotations, tuple):
                    raise MissingClienOROrder(detail=f"{cotations[0]} with id {cotations[1]} doesn't exist.")

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
        return serializer

    def partial_update(self, request, pk=None, *args, **kwargs):
        itinerary_data = request.data
        itinerary = self.get_object()
        segments = itinerary_data.pop("segments", None)
        if segments is not None:
            for segment in segments:
                self.update_m2m_field(itinerary, segment)
        
        self.update_without_relation(itinerary, itinerary_data)
        return Response(self.get_serializer(itinerary).data)
    
    def update_without_relation(self, instance, data):
        if data:
            for key, value in data.items():
                setattr(instance, key, value)

    def update_m2m_field(self,itinerary, segment):
        itinerary_segment = itinerary.segments.filter(id=segment["id"]).first()

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
        instance.segments.all().delete()
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
    
    @action(methods=["put"], url_path="assign/(?P<client_id>\d+)", detail=True,)
    def assign(self, request, client_id, *args, **kwargs):
        qs = self.get_queryset().get(**kwargs)
        serialized_data = self.get_serializer(qs).data
        segments = serialized_data.pop('segments')
        simple_data = self._get_simple_data(serialized_data)
        complex_data = self.get_complex_data(serialized_data)
        segments_data = self.get_segments_info(segments)

        c_id = [{"id": client_id}]
        o_id = complex_data.get('order', None)
        _ = self.create_and_save_itinerary(simple_data, segments_data, client_id=c_id, order_id=o_id)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(methods=['get'], url_path="client/(?P<client_id>\d+)", detail=False)
    def client(self, request, client_id, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        try:
            qs = qs.filter(client_id=client_id)
        except:
            return qs.none()
        serializer = self.get_serializer(qs, many=True)
        return self.paginate_and_response(serializer)
    
    @action(methods=['get'], url_name="templates/", detail=False)
    def templates(self, request, *args, **kwargs):
        qs = self.get_queryset(*args, **kwargs)
        serializer = self.get_serializer(qs.filter(client__isnull=True), many=True)
        return self.paginate_and_response(serializer)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['post'], detail=True)
    def copy(self, request, *args, **kwargs):
        qs = self.get_queryset().get(**kwargs) # Itinerary.objects.get(pk=self.kwargs.get('pk',None))
        serialized_data = self.get_serializer(qs).data

        segments = serialized_data.pop('segments',)
        simple_data = self._get_simple_data(serialized_data)
        complex_data = self.get_complex_data(serialized_data)
        segments_data = self.get_segments_info(segments)

        c_id = complex_data.get('client', None)
        o_id = complex_data.get('order', None)
        _ = self.create_and_save_itinerary(simple_data, segments_data, client_id=c_id, order_id=o_id)
        return Response(status=status.HTTP_201_CREATED)
    
    def _get_simple_data(self, serialized_data):
        fields = [field for field, _ in ItineraryValidator.__annotations__.items() if not isinstance(_, typing._GenericAlias)]
        return self._get_fields_of_simple_type_data(serialized_data, fields)

    def get_complex_data(self, serialized_data):
        fields = [field for field, _ in ItineraryValidator.__annotations__.items() if isinstance(_, typing._GenericAlias) and field != "segments"]
        return self._get_fields_of_type_list_data(serialized_data, fields)

    
    def get_segments_info(self, segments) -> List:
        output = list()
        fields_of_simple_type, fields_of_type_list = self._get_validator_field_with_list_as_type(ItinerarySegmentValidator)
        for seg in segments: # serialized_data["segments"]
            temp1 = self._get_fields_of_type_list_data(seg, fields_of_type_list)
            temp2 = self._get_fields_of_simple_type_data(seg, fields_of_simple_type)
            output.append({**temp1, **temp2})
        return output

    def _get_validator_field_with_list_as_type(self, validator: object):
        fields_of_simple_type, fields_of_type_list = [], []
        for field_name, field_type in validator.__annotations__.items():
            if not self.is_pydantic_complex_type(field_type, list):
                fields_of_simple_type.append(field_name)
            else:
                fields_of_type_list.append(field_name)
        return fields_of_simple_type, fields_of_type_list
    
    @staticmethod
    def is_pydantic_complex_type(field_type, t):
        try:
            if issubclass(getattr(field_type, "__origin__"), t):
                return True
        except:
            return False

    @staticmethod
    def _get_fields_of_type_list_data(data, cfields: List[Dict]) -> Dict:
        output = dict()
        # breakpoint()
        for field in cfields:
            try:
                field_data = data.get(field)
                if isinstance(field_data, list):
                    output[field] = []
                    for fd in field_data:
                        output[field].append({"id": fd["id"]})
                else:
                    output[field] = [{"id": data.get(field)["id"]}]
            except:
                output[field] = []
        return output

    @staticmethod
    def _get_fields_of_simple_type_data(data, sfields: List) -> dict:
        output = dict()
        for field in sfields:
            output[field] = data.get(field, None)
        return output
    
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
                    try:
                        obj =  model.objects.get(id=index)
                    except:
                        return v, index
                    output[k].append(obj)
        return output
    
    @staticmethod
    def _get_location(segment, pos):
        loc = segment.pop(pos)
        if loc and loc is not None:
            return MadaCountry.objects.get(id=loc[-1].get("id"))
        return None
