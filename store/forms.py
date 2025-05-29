from django import forms
from .models import Refund

class RefundForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=True)