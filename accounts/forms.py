from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField


User = get_user_model()

# -----------------------   Admin Forms  ---------------------------------------------------


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "surname",
            "password1",
            "password2",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password1","Şifrələr arasında ziddiyyət var.")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "surname",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
        ]

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.ModelForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control", "placeholder": filed.title})

    def get_user(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        return authenticate(email=email, password=password)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            raise forms.ValidationError("No account with this email.")

        if not user.check_password(password):
            raise forms.ValidationError("Password is wrong.")

        if not user.is_active:
            raise forms.ValidationError("This account is not activate.")

        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "name", "surname", "password", "password_confirm")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {"name": "Name", "surname": "Surname", "email": "Email", "password": "Password", "password_confirm": "Password confirm"}
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control", "placeholder": placeholders[filed], "required": True})

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        if len(password) < 8:
            raise forms.ValidationError("Password should contain 8 character at least.")
        if not any(i.isdigit() for i in password):
            raise forms.ValidationError("The password must contain at least 1 number and letters.")
        if password != password_confirm:
            raise forms.ValidationError("Passwords should match.")
        return self.cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data.pop("password_confirm")

        user = User.objects.create(
            **self.cleaned_data, is_active=False
        )
        user.set_password(password)
        user.save()
        return user




