from django import forms
from .models import PlantOperator, Request, Customer
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class Account(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class AdminUpdatePlantOperator(forms.ModelForm):
    class Meta:
        model = PlantOperator
        fields = [
            'skill',
            'salary',
            'hired',
        ]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'category',
            'machinery_no',
            'machinery_name',
            'machinery_model',
            'machinery_brand',
            'problem_description',
            'customer',
            'plant_operator',
            'cost',
            'status',
        ]

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class PlantOperatorUpdateStatus(forms.ModelForm):
    class Meta:
        model = PlantOperator
        fields = [
            'username',
            'email',
            'phone',
            'location',
            'image',
            'skill'
        ]

class PlantOperatorUpdateForm(forms.ModelForm):
    class Meta:
        model = PlantOperator
        fields = '__all__'
