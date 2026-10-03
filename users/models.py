from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "Користувач"),
        ("admin", "Адміністратор"),
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    cover = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        max_length=500,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.username


