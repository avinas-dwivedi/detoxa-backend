from ..models.transactions_models import Transactions
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class SubscriptionType:
        choices = (('Parent', 'Parent'), ('Corporate', 'Corporate'), ('School', 'School'),
                   ('Society', 'Society'))

    subscription_type = serializers.ChoiceField(choices=SubscriptionType.choices)

    """
    Serializer for Transaction model
    """

    class Meta:
        model = Transactions
        fields = ['tenure', 'subscription_type', 'amount']


class UpdateTransactionSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    payment_id = serializers.CharField()
    signature = serializers.CharField()

    class Meta:
        fields = ['order_id', 'payment_id', 'signature']