from django.contrib import admin
from django.contrib.admin import action

from .models import Product, Category, Client, Order

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    # fields = ('name', 'category', 'price', 'stock', 'available')
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = ['add50']

    @action
    def add50(self, request, queryset):
        for stocks in queryset.all():
            queryset.update(stock = int(stocks.stock)+50)
        return queryset

    add50.short_description = 'Add 50 in stock'


class ClientAdmin(admin.ModelAdmin):
    # fields = ('first_name', 'price', 'stock', 'available')
    # fields = ('first_name', 'last_name', 'city', 'interested_in')
    list_display = ('first_name', 'last_name', 'city', 'interested_in_list')


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Category)
# admin.site.register(Client)
admin.site.register(Order)

