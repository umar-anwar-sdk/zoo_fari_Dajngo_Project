from django import forms

class MyForm(forms.Form):
    first = forms.CharField(max_length=100)
    last = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)  # Assuming phone is optional
    address = forms.CharField(max_length=200)  # Make sure address field is defined
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=10)
    adult = forms.IntegerField()
    kids = forms.IntegerField()


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Email or Username',
        widget=forms.TextInput(attrs={'placeholder': 'Email or Username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(required=False, initial=False, label='Remember me')
