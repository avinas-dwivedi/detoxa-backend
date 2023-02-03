from django.db import models
from detoxa_services.models.kits_models import Kit
from detoxa_services.models.users import Address,Users

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Dispatched', 'Dispatched'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),

)


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_items = models.JSONField()
    order_status = models.CharField(choices=ORDER_STATUS, max_length=255)
    order_total_without_gst = models.FloatField()
    order_gst = models.FloatField()
    order_total = models.FloatField()
    order_discount = models.FloatField(default=0)
    is_coupon_applied = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=25, null=True, blank=True)
    order_updated_at = models.DateTimeField(auto_now=True)
    order_created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    item = models.ForeignKey(Kit,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart_updated_at = models.DateTimeField(auto_now=True)
    cart_created_at = models.DateTimeField(auto_now_add=True)

