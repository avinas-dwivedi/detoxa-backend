from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'services'
        managed = True


class Testimonials(models.Model):
    customer_name = models.CharField(max_length=100)
    service = models.ForeignKey(Services, db_column='service_id', on_delete=models.CASCADE,
                                related_name='fk_service_id', null=True)
    picture_url = models.TextField(null=True)
    testimonial = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'testimonials'
        managed = True
