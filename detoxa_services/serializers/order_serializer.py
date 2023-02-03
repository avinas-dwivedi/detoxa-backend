from random import choices
from rest_framework import serializers
from detoxa_services.models.kits_models import Kit
from detoxa_services.models.orders import Cart, Order
from detoxa_services.models.users import Address, Users
from detoxa_services.models.transactions_models import Invoice, OrderTransaction

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Dispatched', 'Dispatched'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),

)


class GetOrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        order_items = obj.order_items
        order_items_arr = []
        for order_item in order_items:
            for j in order_items:
                kit_obj = Kit.objects.filter(id=order_items[j]['id'])
                for i in kit_obj:
                    order_items_arr.append({'id': i.id, 'name': i.name,
                                            'price': i.price, 'image': i.image_1,
                                            'quantity': order_items[order_item]['quantity']})
            return order_items_arr

    def get_invoice_url(self, obj):
        try:
            invoice_obj = Invoice.objects.get(order__order=obj.id)
            return invoice_obj.invoice_url
        except:
            return None


class CreateOrderSerializer(serializers.Serializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    order_items = serializers.JSONField()
    order_status = serializers.ChoiceField(choices=ORDER_STATUS)
    order_gst = serializers.FloatField()
    order_discount = serializers.FloatField()
    order_total_without_gst = serializers.FloatField()
    order_total = serializers.FloatField()
    is_coupon_applied = serializers.BooleanField(default=False)
    coupon_code = serializers.CharField(max_length=255,required=False,allow_null=True)



class OrderTransactionSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    payment_gateway = serializers.CharField(max_length=20, default='Razorpay')
    payment_id = serializers.CharField(max_length=100, required=False)
    signature = serializers.CharField(max_length=100, required=False)


class OrderListingForAdminSeriailizer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    class Meta:
        model = OrderTransaction
        fields = '__all__'
        depth = 4
        # read_only_fields = (fields,)
        # exclude = ('order__order_items',)

    def get_order_items(self, obj):
        order_items = obj.order.order_items
        order_items_arr = []
        for order_item in order_items:
            kit_obj = Kit.objects.get(id=order_items[order_item]['id'])
            order_items_arr.append({'id':kit_obj.id, 'name':kit_obj.name, 'price':kit_obj.price,'image':kit_obj.image_1, 'quantity':order_items[order_item]['quantity']})
        return order_items_arr

    def get_invoice_url(self, obj):
        try:
            invoice_url = Invoice.objects.get(order=obj).invoice_url
            return invoice_url
        except:
            return None


    

class CartSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Kit.objects.all())
    quantity = serializers.IntegerField()

class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    
class GetCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth = 4
        read_only_fields = (fields,)

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 4
        read_only_fields = (fields,)




