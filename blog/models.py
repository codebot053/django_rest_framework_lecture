from django.db import models
from user.models import User
# Create your models here.

class Category(models.Model):
    class Meta:
        db_table = "category"

    name = models.CharField("카테고리 이름", max_length=50)
    introduction = models.CharField('설명',max_length=255)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    class Meta:
        db_table = "article"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("글 제목", max_length=50)
    category = models.ManyToManyField(to="Category", verbose_name="카테고리")
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name