from django.conf import settings
from django.db import models


class Notification(models.Model):
    class ActionType(models.TextChoices):
        LIKE = "like", "Лайк"
        COMMENT = "comment", "Коментар"
        SHARE = "share", "Поширення"
        FOLLOW = "follow", "Підписка"
        REPLY = "reply", "Відповідь"

    # Хто виконав дію
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )

    # Хто отримує сповіщення
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )

    # Тип дії
    action_type = models.CharField(
        max_length=20,
        choices=ActionType.choices,
    )

    # Пост, під яким відбулася дія
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )

    # Коментар, якщо сповіщення стосується коментаря
    comment = models.ForeignKey(
        "posts.Comment",
        on_delete=models.SET_NULL,
        related_name="notifications",
        null=True,
        blank=True,
    )

    # Чи прочитане сповіщення
    is_read = models.BooleanField(default=False)

    # Дата й час створення
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.actor} → {self.recipient}: "
            f"{self.get_action_type_display()}"
        )
