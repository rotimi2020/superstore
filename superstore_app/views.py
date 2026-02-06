# dashboard/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum, Avg ,F, FloatField
from django.db.models.functions import TruncDate
from .models import SuperstoreDashboard  # Your sales model
import math
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages


def dashboard(request):
    qs = SuperstoreDashboard.objects.all()
    #diabetic_count = Diabetes_Patient.objects.filter(outcome=True).count()
    #non_diabetic_count = total_patients - diabetic_count
    
    #avg_glucose = Diabetes_Patient.objects.aggregate(Avg('glucose'))['glucose__avg'] or 0
    #avg_bmi = Diabetes_Patient.objects.aggregate(Avg('bmi'))['bmi__avg'] or 0
    #avg_age = Diabetes_Patient.objects.aggregate(Avg('age'))['age__avg'] or 0
    
    # Age distribution
    # age_groups = {
    #     '20-30': Diabetes_Patient.objects.filter(age__gte=20, age__lt=30).count(),
    #     '30-40': Diabetes_Patient.objects.filter(age__gte=30, age__lt=40).count(),
    #     '40-50': Diabetes_Patient.objects.filter(age__gte=40, age__lt=50).count(),
    #     '50-60': Diabetes_Patient.objects.filter(age__gte=50, age__lt=60).count(),
    #     '60+': Diabetes_Patient.objects.filter(age__gte=60).count(),
    # }
    # Calculate KPIs
    kpi_totals = qs.aggregate(
        total_sales=Sum('sales'),
        total_profit=Sum('profit'),
        avg_sale_per_order=Avg('sales'),
        avg_profit_per_order=Avg('profit')
    )

    # Sales by Category for Bar Chart
    sales_by_category_qs = qs.values('category').annotate(total_sales=Sum('sales')).order_by('category')
    categories = [item['category'] for item in sales_by_category_qs]
    category_sales = [float(item['total_sales']) for item in sales_by_category_qs]
    
    from collections import defaultdict

    # Create a dict to aggregate sales by date safely
    sales_dict = defaultdict(float)

    for row in qs:
        if row.order_date:  # skip None or invalid dates
            sales_dict[row.order_date] += float(row.sales)

    # Sort dates
    sorted_dates = sorted(sales_dict.keys())

    line_dates = [d.strftime('%Y-%m-%d') for d in sorted_dates]
    line_sales = [sales_dict[d] for d in sorted_dates]

    # Profit by Category for Doughnut Chart
    profit_by_category_qs = qs.values('category').annotate(total_profit=Sum('profit')).order_by('category')
    profit_categories = [item['category'] for item in profit_by_category_qs]
    category_profits = [float(item['total_profit']) for item in profit_by_category_qs]




    
    context = {
        'total_patients': qs,
        'totalSales': kpi_totals['total_sales'] or 0,
        'totalProfit': kpi_totals['total_profit'] or 0,
        'avgSalePerOrder': kpi_totals['avg_sale_per_order'] or 0,
        'avgProfitPerOrder': kpi_totals['avg_profit_per_order'] or 0,
        'profit_categories': profit_categories,
        'category_profits': category_profits,
        'bar_categories': categories,
        'bar_category_sales': category_sales,
        'line_dates': line_dates,
        'line_sales': line_sales,
        # 'diabetic_count': diabetic_count,
        # 'non_diabetic_count': non_diabetic_count,
        # 'diabetic_percentage': round((diabetic_count / total_patients * 100), 1) if total_patients > 0 else 0,
        # 'avg_glucose': round(avg_glucose, 1),
        # 'avg_bmi': round(avg_bmi, 1),
        # 'avg_age': round(avg_age, 1),
        # 'age_groups': age_groups,
    }
    
    return render(request, 'superstore_app/dashboard.html', context)


def analytics(request):
    total_patients = SuperstoreDashboard.objects.count()  # Add total_patients

       # Aggregate sales by segment
    sales_by_segment = (
        SuperstoreDashboard.objects
        .values('segment')                  # Group by Segment
        .annotate(total_sales=Sum('sales')) # Sum sales per segment
        .order_by('segment')
    )

    # Prepare lists for Chart.js
    segment_labels = [entry['segment'] for entry in sales_by_segment]
    segment_sales = [float(entry['total_sales']) for entry in sales_by_segment]


       # Right chart: Profit by Sub-Category
    profit_by_subcat = (
        SuperstoreDashboard.objects
        .values('sub_category')
        .annotate(total_profit=Sum('profit'))
        .order_by('sub_category')
    )
    subcat_labels = [entry['sub_category'] for entry in profit_by_subcat]
    subcat_profit = [float(entry['total_profit']) for entry in profit_by_subcat]


        # Line chart: Profit Over Time
    profit_over_time = (
        SuperstoreDashboard.objects
        .values('order_date')
        .annotate(total_profit=Sum('profit'))
        .order_by('order_date')
    )
    profit_dates = [entry['order_date'].strftime('%Y-%m-%d') for entry in profit_over_time]
    profit_values = [float(entry['total_profit']) for entry in profit_over_time]

      # Scatter Chart: Quantity vs Sales
    quantity_sales_qs = SuperstoreDashboard.objects.values('quantity', 'sales')
    quantity_sales_data = [
        {'x': float(entry['quantity']), 'y': float(entry['sales'])}
        for entry in quantity_sales_qs
    ]
    

    # Scatter chart: Profit vs Discount
    profit_discount_qs = SuperstoreDashboard.objects.values('discount', 'profit')

    profit_discount_data = [
        {
            'x': float(row['discount']),
            'y': float(row['profit']),
        }
        for row in profit_discount_qs
        if row['discount'] is not None and row['profit'] is not None
    ]


    # Map: Sales & Profit by State
    state_performance = (
        SuperstoreDashboard.objects
        .values('state')
        .annotate(
            total_sales=Sum('sales'),
            total_profit=Sum('profit')
        )
        .order_by('state')
    )

    state_map_data = {
        entry['state']: {
            'sales': float(entry['total_sales'] or 0),
            'profit': float(entry['total_profit'] or 0)
        }
        for entry in state_performance
    }


    # Bubble chart: Profit vs Discount
    profit_discount = (
        SuperstoreDashboard.objects
        .values('discount', 'profit')
    )

    bubble_data = []
    for item in profit_discount:
        bubble_data.append({
            'x': float(item['discount']),   # X-axis → Discount
            'y': float(item['profit']),     # Y-axis → Profit
            'r': 6                           # Bubble size (fixed for now)
        })



#     # BMI categories
#     bmi_categories = {
#         'Underweight': Diabetes_Patient.objects.filter(bmi__lt=18.5).count(),
#         'Normal': Diabetes_Patient.objects.filter(bmi__gte=18.5, bmi__lt=25).count(),
#         'Overweight': Diabetes_Patient.objects.filter(bmi__gte=25, bmi__lt=30).count(),
#         'Obese': Diabetes_Patient.objects.filter(bmi__gte=30).count(),
#     }

#     # Glucose levels
#     glucose_ranges = {
#         'Normal (<100)': Diabetes_Patient.objects.filter(glucose__lt=100).count(),
#         'Prediabetes (100-125)': Diabetes_Patient.objects.filter(glucose__gte=100, glucose__lt=126).count(),
#         'Diabetes (≥126)': Diabetes_Patient.objects.filter(glucose__gte=126).count(),
#     }

#     # Risk factors by age
#     age_risk = []
#     for age in range(20, 81, 10):
#         age_patients = Diabetes_Patient.objects.filter(age__gte=age, age__lt=age+10)
#         total = age_patients.count()
#         diabetic = age_patients.filter(outcome=True).count()
#         age_risk.append({
#             'age_group': f"{age}-{age+9}",
#             'total': total,
#             'diabetic': diabetic,
#             'percentage': round((diabetic / total * 100), 1) if total > 0 else 0
#         })

    context = {
        'total_patients': total_patients,
        'segment_labels': segment_labels,
        'segment_sales': segment_sales,
        'subcat_labels': subcat_labels,     
        'subcat_profit': subcat_profit, 
        'profit_dates': profit_dates,     # for line chart x-axis
        'profit_values': profit_values,
        'quantity_sales_data': quantity_sales_data,
        'profit_discount_data': profit_discount_data,
        'state_map_data': state_map_data,
        'bubble_data': bubble_data,
    }

    return render(request, 'superstore_app/analytics.html', context)



def sales(request):
    # Fetch all sales records ordered by order_date descending
    sales_queryset = SuperstoreDashboard.objects.all().order_by('-order_date')

    # Paginate the sales table
    paginator = Paginator(sales_queryset, 100)  # 10 rows per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate KPIs
    kpi_totals = sales_queryset.aggregate(
        total_sales=Sum('sales'),
        total_profit=Sum('profit'),
        avg_sale_per_order=Avg('sales'),
        avg_profit_per_order=Avg('profit')
    )

    context = {
        'sales_data': page_obj.object_list,
        'page_obj': page_obj,
        'totalSales': kpi_totals['total_sales'] or 0,
        'totalProfit': kpi_totals['total_profit'] or 0,
        'avgSalePerOrder': kpi_totals['avg_sale_per_order'] or 0,
        'avgProfitPerOrder': kpi_totals['avg_profit_per_order'] or 0,
    }
    return render(request, 'superstore_app/sales.html', context)

