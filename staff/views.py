from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from superstore_app.models import SuperstoreDashboard
from django.core.paginator import Paginator
from django.db.models import Sum, Avg ,F, FloatField
from .forms import SalesForm

# Only staff (not superuser) can access
def staff_only(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

# Staff login
def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff and not user.is_superuser:
            login(request, user)
            return redirect('staff:staff_dashboard')
        else:
            messages.error(request, 'Invalid staff credentials')
    return render(request, 'staff/login.html')

# Staff logout
def staff_logout(request):
    logout(request)
    return redirect('staff:staff_login')

# Staff dashboard
@login_required
@user_passes_test(staff_only)
def staff_dashboard(request):
    total_sales = SuperstoreDashboard.objects.count()
    return render(request, 'staff/dashboard.html', {'total_sales': total_sales})

# List all sales
@login_required
@user_passes_test(staff_only)
def staff_sales_list(request):
    sales_queryset = SuperstoreDashboard.objects.all()


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
    return render(request, 'staff/sales_list.html', context)

# Create new sale
@login_required
@user_passes_test(staff_only)
def staff_sales_create(request):
    form = SalesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('staff:staff_sales_list')
    return render(request, 'staff/sales_form.html', {'form': form})

# detail page
@login_required
@user_passes_test(staff_only)
def staff_sales_detail(request, pk):
    sale = get_object_or_404(SuperstoreDashboard, pk=pk)
    return render(request, 'staff/sales_detail.html', {'sale': sale})


# Update sale
@login_required
@user_passes_test(staff_only)
def staff_sales_update(request, pk):
    sale = get_object_or_404(SuperstoreDashboard, pk=pk)
    form = SalesForm(request.POST or None, instance=sale)
    if form.is_valid():
        form.save()
        return redirect('staff:staff_sales_list')
    return render(request, 'staff/sales_form.html', {'form': form})

# Delete sale
@login_required
@user_passes_test(staff_only)
def staff_sales_delete(request, pk):
    sale = get_object_or_404(SuperstoreDashboard, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('staff:staff_sales_list')
    return render(request, 'staff/confirm_delete.html', {'sale': sale})
   