from django.db import models


class Feedback(models.Model):
    """
    Feedback model
    """

    rating = models.IntegerField(default=0)
    comment = models.TextField()
    email = models.EmailField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
