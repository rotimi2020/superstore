from django.contrib import admin
from .models import SuperstoreDashboard


@admin.register(SuperstoreDashboard)
class SuperstoreDashboardAdmin(admin.ModelAdmin):

    list_display = [
        'order_date',
        'ship_date',
        'region',
        'state', 
        'category',
        'sub_category',
        'segment',
        'sales',
        'profit',
        'quantity',
        'discount',
    ]

    list_filter = [
        'order_date',
        'region',
        'category',
        'segment',
        'ship_mode',
    ]

    search_fields = [
        'city',
        'state',
        'category',
        'sub_category',
    ]

    # 👇 THIS controls horizontal vs vertical layout in the edit page
    fieldsets = (
        ('Dates', {
            'fields': (('order_date', 'ship_date'),)
        }),
        ('Geography', {
            'fields': (('region', 'state', 'city'),)
        }),
        ('Business Info', {
            'fields': (('segment', 'category', 'sub_category', 'ship_mode'),)
        }),
        ('Metrics', {
            'fields': (('sales', 'profit', 'quantity', 'discount'),)
        }),
    )
