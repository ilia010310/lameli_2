from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Product, Category, ProductImages
from django.utils.safestring import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записей
    """
    list_display = ['image_show', 'name', 'slug', 'status', 'price']
    list_editable = ['status']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', ]
    ordering = ['-publish']
    inlines = [ProductImageInline]

    def image_show(self, obj):
        return mark_safe("<img src='{}' width='60' />".format(obj.avatar.url))

    def has_delete_permission(self, request, obj=None):
        return False

    image_show.__name__ = "Картинка"


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}
