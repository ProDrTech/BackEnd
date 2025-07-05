from rest_framework import serializers
from order.models.order import PaymentSession

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSession
        fields = '__all__'