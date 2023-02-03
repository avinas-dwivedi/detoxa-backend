from django.db import models

from detoxa_services.models.orders import Order
from ..models.users import Users


class Transactions(models.Model):
    """
    Transactions Model
    """

    class TransactionStatus:
        choices = (('Pending', 'Pending'), ('Success', 'Success'), ('Declined ', 'Declined'),
                   ('Retry ', 'Retry'))

    class SubscriptionType:
        choices = (('Parent', 'Parent'), ('Corporate', 'Corporate'), ('School', 'School'),
                   ('Society', 'Society'))

    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    tenure = models.CharField(max_length=100)
    subscription_type = models.CharField(max_length=100, choices=SubscriptionType.choices, null=True)
    payment_gateway = models.CharField(max_length=20, default='Razorpay')
    currency = models.CharField(max_length=20, default='INR')
    order_id = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length=100, null=True)
    signature = models.CharField(max_length=100, null=True)
    transaction_datetime = models.DateTimeField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default='Pending')
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    amount = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class OrderTransaction(models.Model):
    """
    OrderTransaction Model
    """
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    payment_gateway = models.CharField(max_length=20, default='Razorpay')
    payment_id = models.CharField(max_length=100, null=True)
    signature = models.CharField(max_length=100, null=True)
    transaction_datetime = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    """
    Invoice Model
    """
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    invoice_amount = models.CharField(max_length=100, null=True)
    invoice_url = models.URLField()