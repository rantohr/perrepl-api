from .models import Activity, ActivityPrice

from rest_framework import serializers
from apps.mada_countries.serializers import MadaCountrySerializer
from apps.suppliers.serializers import SupplierSerializer

class ActivityPriceSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    class Meta:
        model = ActivityPrice
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    location = MadaCountrySerializer(required=True)
    prices = serializers.SerializerMethodField() # ActivityPriceSerializer(many=True, required=False)

    def price_activity(self, activity_prices: ActivityPrice, optimum:str='min'):
        if optimum == 'min':
            m_ap = min(activity_prices, key=lambda x: x.price)
        if optimum == 'max':
            m_ap = max(activity_prices, key=lambda x: x.price)
        return ActivityPriceSerializer(m_ap, required=False).data
    
    def get_prices(self, instance: Activity):
        supplier_id = self.context.get('supplier_id', None)
        activity_prices = instance.prices.all()
        if supplier_id:
            ap = activity_prices.filter(supplier_id=supplier_id)
            return ActivityPriceSerializer(ap, many=True, required=False).data
        
        if self.context.get('minimal_price', None):
            return self.price_activity(activity_prices, optimum='min')
        
        if self.context.get('maximal_price', None):
            return self.price_activity(activity_prices, optimum='max')
        
    class Meta:
        model = Activity
        # fields = '__all__'
        exclude = ('user',)
