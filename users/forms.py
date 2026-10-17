from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Email",
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # прибираємо підказки під полями
        for field in self.fields.values():
            field.help_text = ""

        # підписи та підказки всередині полів
        self.fields["username"].label = "Ім'я користувача"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторіть пароль"

        self.fields["username"].widget.attrs["placeholder"] = "Наприклад, ivan_petrenko"
        self.fields["email"].widget.attrs["placeholder"] = "you@example.com"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Цей email уже зареєстрований.")

        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "avatar",
            "cover",
        ]

        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "email": "Email",
            "bio": "Про себе",
            "avatar": "Аватар",
            "cover": "Обкладинка",
        }

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Цей email уже використовує інший акаунт.")

        return email