from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Restaurant
from django.utils.translation import ugettext_lazy as _

class ShopRegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Shop Name"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data



class RestaurantRegisterForm(forms.Form):
    shop_name = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Restaurant Name."}),label=_(""))


    business_address = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Business address.", 'id': 'reg_location'}), label=_(""))

    location_id = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs= {'class': 'form-control', 'type':'hidden',
                                    'id': 'location_id_reg'}), label=_(""))

    username = forms.CharField(widget=forms.TextInput({'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Username."}), label=_(""),
                                 )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pushDown ', 'type':'password',
                                   'placeholder':"Password."}), label=_(""))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pushDown', 'type':'password',
                                   'placeholder':"Password again."}), label=_(""))

    def clean_location_id(self):
        try:
            restaurant = Restaurant.objects.get(location_id__iexact=self.cleaned_data['location_id'])
        except Restaurant.DoesNotExist:
            return self.cleaned_data['location_id']
        raise forms.ValidationError(_("The location_id already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data



class RestaurantLoginForm(forms.Form):
  
    username = forms.CharField(widget=forms.TextInput({'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Username."}), label=_(""),
                                 )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control ', 'type':'password',
                                   'placeholder':"Password."}), label=_(""))


