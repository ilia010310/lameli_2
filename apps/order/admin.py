from django.contrib import admin
from apps.order.models import Status, ProductsInOrder, Order


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 0

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created', 'updated']
    ordering = ['id']

# @admin.register(ItemsInOrder)
# class ItemsInOrderAdmin(admin.ModelAdmin):
#     list_display = ['order', 'item', 'quantity', 'created', 'updated' ]
#     ordering = ['id']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'customer_name', 'customer_email',
                    'customer_inn', 'status', 'created', 'updated' ]
    ordering = ['status']
    inlines = [ProductsInOrderInline]

