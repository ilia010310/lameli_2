from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Product, Category


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записей
    """
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}

