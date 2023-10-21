from django.contrib import admin
from sales.models import Commission


class ComissionAdmin(admin.ModelAdmin):
    list_display = ['day_week', 'min', 'max']
    ordering = ['day_week', 'min', 'max']
    search_fields = ['day_week']
    list_filter = ['day_week']


admin.site.register(Commission, ComissionAdmin)
