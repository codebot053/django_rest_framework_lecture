from unicodedata import category
from django.contrib import admin
from blog.models import Category
from blog.models import Article
# Register your models here.

admin.site.register(Category)
admin.site.register(Article)