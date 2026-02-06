from django.db import models


class SuperstoreDashboard(models.Model):

    SHIP_MODE_CHOICES = [
        ('Second Class', 'Second Class'),
        ('Standard Class', 'Standard Class'),
        ('First Class', 'First Class'),
        ('Same Day', 'Same Day'),
    ]

    SEGMENT_CHOICES = [
        ('Consumer', 'Consumer'),
        ('Corporate', 'Corporate'),
        ('Home Office', 'Home Office'),
    ]

    REGION_CHOICES = [
        ('South', 'South'),
        ('West', 'West'),
        ('Central', 'Central'),
        ('East', 'East'),
    ]

    CATEGORY_CHOICES = [
        ('Furniture', 'Furniture'),
        ('Office Supplies', 'Office Supplies'),
        ('Technology', 'Technology'),
    ]

    SUB_CATEGORY_CHOICES = [
        ('Bookcases', 'Bookcases'),
        ('Chairs', 'Chairs'),
        ('Labels', 'Labels'),
        ('Tables', 'Tables'),
        ('Storage', 'Storage'),
        ('Furnishings', 'Furnishings'),
        ('Art', 'Art'),
        ('Phones', 'Phones'),
        ('Binders', 'Binders'),
        ('Appliances', 'Appliances'),
        ('Paper', 'Paper'),
        ('Accessories', 'Accessories'),
        ('Envelopes', 'Envelopes'),
        ('Fasteners', 'Fasteners'),
        ('Supplies', 'Supplies'),
        ('Machines', 'Machines'),
        ('Copiers', 'Copiers'),
    ]

    STATE_CHOICES = [
        ('Kentucky', 'Kentucky'),
        ('California', 'California'),
        ('Florida', 'Florida'),
        ('North Carolina', 'North Carolina'),
        ('Washington', 'Washington'),
        ('Texas', 'Texas'),
        ('Wisconsin', 'Wisconsin'),
        ('Utah', 'Utah'),
        ('Nebraska', 'Nebraska'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Illinois', 'Illinois'),
        ('Minnesota', 'Minnesota'),
        ('Michigan', 'Michigan'),
        ('Delaware', 'Delaware'),
        ('Indiana', 'Indiana'),
        ('New York', 'New York'),
        ('Arizona', 'Arizona'),
        ('Virginia', 'Virginia'),
        ('Tennessee', 'Tennessee'),
        ('Alabama', 'Alabama'),
        ('South Carolina', 'South Carolina'),
        ('Oregon', 'Oregon'),
        ('Colorado', 'Colorado'),
        ('Iowa', 'Iowa'),
        ('Ohio', 'Ohio'),
        ('Missouri', 'Missouri'),
        ('Oklahoma', 'Oklahoma'),
        ('New Mexico', 'New Mexico'),
        ('Louisiana', 'Louisiana'),
        ('Connecticut', 'Connecticut'),
        ('New Jersey', 'New Jersey'),
        ('Massachusetts', 'Massachusetts'),
        ('Georgia', 'Georgia'),
        ('Nevada', 'Nevada'),
        ('Rhode Island', 'Rhode Island'),
        ('Mississippi', 'Mississippi'),
        ('Arkansas', 'Arkansas'),
        ('Montana', 'Montana'),
        ('New Hampshire', 'New Hampshire'),
        ('Maryland', 'Maryland'),
        ('District of Columbia', 'District of Columbia'),
        ('Kansas', 'Kansas'),
        ('Vermont', 'Vermont'),
        ('Maine', 'Maine'),
        ('South Dakota', 'South Dakota'),
        ('Idaho', 'Idaho'),
        ('North Dakota', 'North Dakota'),
        ('Wyoming', 'Wyoming'),
        ('West Virginia', 'West Virginia'),
    ]

    # =========================
    # TIME (KEEP BOTH – IMPORTANT)
    # =========================
    order_date = models.DateField('Order Date')
    ship_date = models.DateField('Ship Date')

    # =========================
    # GEOGRAPHY
    # =========================
    region = models.CharField('Region', max_length=10, choices=REGION_CHOICES)
    state = models.CharField('State', max_length=50, choices=STATE_CHOICES, blank=True)
    city = models.CharField('City', max_length=100)

    # =========================
    # BUSINESS DIMENSIONS
    # =========================
    segment = models.CharField('Segment', max_length=20, choices=SEGMENT_CHOICES)
    category = models.CharField('Category', max_length=20, choices=CATEGORY_CHOICES)
    sub_category = models.CharField('Sub Category', max_length=30, choices=SUB_CATEGORY_CHOICES)
    ship_mode = models.CharField('Ship Mode', max_length=20, choices=SHIP_MODE_CHOICES)

    # =========================
    # METRICS (DASHBOARD-SAFE)
    # =========================
    sales = models.DecimalField('Sales', max_digits=10, decimal_places=3)
    profit = models.DecimalField('Profit', max_digits=10, decimal_places=4)
    quantity = models.IntegerField('Quantity')
    discount = models.DecimalField('Discount', max_digits=3, decimal_places=1)

    class Meta:
        verbose_name = 'Superstore Dashboard'
        verbose_name_plural = 'Superstore Dashboards'
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.order_date} | {self.category} | {self.sales}"



        

