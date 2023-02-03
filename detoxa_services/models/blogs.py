from django.db import models


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    media_url = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_category'
        managed = True


class Author(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'author'
        managed = True


class Blog(models.Model):

    title = models.CharField(max_length=200)
    blog_category = models.ForeignKey(BlogCategory, db_column='blog_category_id', on_delete=models.CASCADE,
                                      related_name='fk_blog_category_id', null=True)
    media_url = models.TextField(null=True)
    published_on = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50, null=True)
    key = models.CharField(max_length=255, null=True)
    para1 = models.TextField(null=True)
    para2 = models.TextField(null=True)
    para3 = models.TextField(null=True)
    para4 = models.TextField(null=True)
    viewed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog'
        managed = True