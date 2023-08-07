from django import forms
from .models import Product, ProductImages

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["owner", "created_at"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ["image"]
        
        widgets ={
            "image": forms.FileInput(attrs={"class": "form-control"})
        }