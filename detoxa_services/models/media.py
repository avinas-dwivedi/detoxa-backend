from django.db import models


class MediaCategory(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media_category'
        managed = True


class Media(models.Model):
    class MediaType(models.Model):
        MEDIATYPE_CHOICES = (('image', 'image'), ('video', 'video'),)

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=20, choices=MediaType.MEDIATYPE_CHOICES, null=True)
    category = models.ForeignKey(MediaCategory, db_column='category_id', on_delete=models.CASCADE,
                                 related_name='fk_category_id', null=True)
    media_url = models.TextField(null=True)
    key = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media'
        managed = True


