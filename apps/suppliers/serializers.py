from rest_framework import serializers
from apps.contacts.serializers import ContactSerializer
from apps.contacts.models import Contact

from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)
    class Meta:
        model = Supplier
        fields = '__all__'
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contacts')
        supplier = Supplier.objects.create(**validated_data)
        
        contacts_list = []
        for contact in contact_data:
            c = Contact.objects.create(**contact)
            contacts_list.append(c)
            
        for c in contacts_list:
            supplier.contacts.add(c)

        return supplier