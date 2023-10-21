from django.contrib import admin

from people.models import Seller, Client


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    ordering = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['email']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    ordering = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['email']


admin.site.register(Seller, SellerAdmin)
admin.site.register(Client, ClientAdmin)
