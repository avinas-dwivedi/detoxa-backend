from django.db import models

NOTIFICATIONS_TYPE = (
    ('Email', 'Email'),
    ('SMS', 'SMS'),
    ('WhatsApp Notification', 'WhatsApp Notification'),
)

class Notifications(models.Model):
    notification_type = models.CharField(choices=NOTIFICATIONS_TYPE,max_length=255)
    title = models.CharField(max_length=255)
    message = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)



class UserDatabaseForNotification(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)