from django.db import models
from .users import Users

STATUS_CHOICES = (('Active', 'Active'), ('Inactive', 'Inactive'))

class UserChildRelation(models.Model):
    parent_user = models.ForeignKey(Users, db_column='parent_user_id', on_delete=models.CASCADE,
                                    related_name='fk_parent_user')
    child_user = models.ForeignKey(Users, db_column='child_user_id', on_delete=models.CASCADE,
                                   related_name='fk_child_user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'user_child_relation'
