from django.db import models


class Banner(models.Model):
    class DeviceType(models.Model):
        DEVICE_TYPE_CHOICES = (('web', 'Web'), ('mobile', 'Mobile'),)

    class SequenceNumber(models.Model):
        SEQUENCE_NUMBER_CHOICES = (
                                    ('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four'), ('five', 'Five'),
                                    ('six', 'Six'), ('seven', 'Seven'), ('eight', 'Eight'),
                                    ('nine', 'Nine'), ('ten', 'Ten')
                                   )

    title = models.CharField(max_length=200)
    device_type = models.CharField(max_length=30, choices=DeviceType.DEVICE_TYPE_CHOICES, null=True)
    picture_url = models.TextField(null=True)
    sequence_number = models.CharField(max_length=30, choices=SequenceNumber.SEQUENCE_NUMBER_CHOICES, null=True)
    start_date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    end_date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    page_link = models.CharField(max_length=200, null=True)
    key = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'banner'
        managed = True