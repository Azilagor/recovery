from django import forms

class PasswordResetForm(forms.Form):
    login = forms.CharField(
        label="Логин",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'i.ivanov'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'i.ivanov@aues.kz'})
    )
    phone_number = forms.CharField(
        label="Номер телефона",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '87071234567'})
    )
