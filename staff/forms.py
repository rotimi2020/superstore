from django import forms
from superstore_app.models import SuperstoreDashboard

class SalesForm(forms.ModelForm):
    """
    ModelForm for staff to add/edit sales records.
    """
    class Meta:
        model = SuperstoreDashboard
        fields = '__all__'  # Or limit fields staff can edit
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'ship_date': forms.DateInput(attrs={'type': 'date'}),
        }
