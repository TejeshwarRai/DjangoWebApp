from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'price', 'stock', 'available')
    actions = ('add50')

    def add50(self, request, queryset):
        for stocks in queryset.all():
            queryset.update(stocks = int(stocks.stock)+50)

    add50.short_description = 'Add 50 in stock'
class ClientAdmin(admin.ModelAdmin):
    fields = ('first_name', '', 'price', 'stock', 'available')

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)

