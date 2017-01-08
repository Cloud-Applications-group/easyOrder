from django import forms
from django.contrib.auth.models import User
from .models import Restaurant


class ShopRegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=("Shop Name"), error_messages={
            'invalid': ("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=("Password (again)"))

    def clean_username(self):
        print "clean_username"
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(("The username already exists. Please try another one."))

    def clean(self):
        print "clean"
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields did not match."))
        return self.cleaned_data

class RestaurantRegisterForm(forms.Form):
    shop_name = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Business name."}),label=(""))


    business_address = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Business address.", 'id': 'reg_location'}), label=(""))

    location_id = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs= {'class': 'form-control', 'type':'hidden',
                                    'id': 'location_id_reg'}), label=(""))

    username = forms.CharField(widget=forms.TextInput({'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Username."}), label=(""),
                                 )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pushDown ', 'type':'password',
                                   'placeholder':"Password."}), label=(""))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pushDown', 'type':'password',
                                   'placeholder':"Password again."}), label=(""))

    def clean_location_id(self):
        try:
            restaurant = Restaurant.objects.get(location_id__iexact=self.cleaned_data['location_id'])
        except Restaurant.DoesNotExist:
            return self.cleaned_data['location_id']
        raise forms.ValidationError(("This location already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("Password fields did not match."))
        return self.cleaned_data

class RestaurantLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput({'class': 'form-control pushDown', 'type':'text',
                                   'placeholder':"Username."}), label=(""),
                                 )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control ', 'type':'password',
                                   'placeholder':"Password."}), label=(""))



class OrderForm(forms.Form):

    content = forms.CharField(widget=forms.TextInput({'id': 'order_content', 'type':'hidden' }), label=(""),
                                 )

    people = forms.CharField(widget=forms.TextInput({'id': 'order_people', 'type': 'hidden'}),
                                      label=(""),
                                      )
    date = forms.CharField(widget=forms.TextInput({'id': 'order_date', 'type': 'hidden'}),
                                      label=(""),
                                      )
    time = forms.CharField(widget=forms.TextInput({'id': 'order_time', 'type': 'hidden'}),
                           label=(""),
                           )

    restaurant_name = forms.CharField(widget=forms.TextInput({'id': 'order_restaurant_name', 'type': 'hidden'}), label=(""),
                              )