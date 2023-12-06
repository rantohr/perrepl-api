from rest_framework import serializers

from apps.mada_countries.serializers import MadaCountrySerializer
from apps.rooms.serializers import RoomSerializer,  RoomPriceSerializer, SimpleRoomSerializer
from apps.images.serializers import ImageSerializer

from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    locations = MadaCountrySerializer(many=True, required=True)
    rooms = serializers.SerializerMethodField() 
    images = serializers.SerializerMethodField()
    hotel_id = serializers.IntegerField(source='id', read_only=True)

    def get_images(self, hotel: Hotel):
        img_qs = hotel.hotel_images.all()
        return ImageSerializer(img_qs, many=True).data

    def price_room(self, rooms, optimum="min"):
        optimum_rooms_price = []
        for room in rooms:
            rp = room.prices.all()
            
            if optimum == "min":
                mrp = min(rp, key=lambda x: x.price)
            else:
                mrp = max(rp, key=lambda x: x.price)

            mrpd = RoomPriceSerializer(mrp, required=False).data
            optimum_rooms_price.append(mrpd)
        return optimum_rooms_price
    
    def get_rooms(self, hotel: Hotel):
        supplier_id = self.context.get("pk", None)
        rooms = hotel.rooms.all()
        if supplier_id:
            rooms_price = []
            for room in rooms:
                rp = room.prices.filter(supplier_id=supplier_id)
                rpd = RoomPriceSerializer(rp, many=True, required=False, read_only=True).data
                rooms_price.append(rpd[0])
            return rooms_price

        if self.context.get('minimal_price', None):
            return self.price_room(rooms, optimum="min")

        if self.context.get('maximal_price', None):
            return self.price_room(rooms, optimum="max")
        
        if self.context.get('rm_price', None):
            return SimpleRoomSerializer(rooms, many=True, read_only=True, required=False).data
        return RoomSerializer(rooms, many=True, read_only=True, required=False).data

    class Meta:
        model = Hotel
        # fields = '__all__'
        exclude = ('id', 'user', )
