from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'unitary_price', 'commission']
    ordering = ['product', 'unitary_price', 'commission']
    search_fields = ['product']
    list_filter = ['product']


admin.site.register(Product, ProductAdmin)
