from rest_framework import serializers
from apps.contacts.serializers import ContactSerializer
from apps.contacts.models import Contact
from apps.images.serializers import ImageSerializer

from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)
    images = serializers.SerializerMethodField()

    def get_images(self, supplier):
        img_qs = supplier.supplier_images.all()
        return ImageSerializer(img_qs, many=True).data
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contacts')
        supplier = Supplier.objects.create(user=self.context['request'].user, **validated_data)
        
        contacts_list = []
        for contact in contact_data:
            c = Contact.objects.create(**contact)
            contacts_list.append(c)
            
        for c in contacts_list:
            supplier.contacts.add(c)

        return supplier
    
    class Meta:
        model = Supplier
        fields = '__all__'
