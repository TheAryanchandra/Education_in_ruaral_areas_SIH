from django import forms
from .models import DownloadableItem

class DownloadableItemForm(forms.ModelForm):
    class Meta:
        model = DownloadableItem
        fields = ['title', 'description', 'file']
