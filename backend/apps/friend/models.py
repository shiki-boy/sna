from django.db import models

from apps.user.models import User
from apps.util.models import AbstractBaseModel


class Friendship(AbstractBaseModel):
    class STATUS_CHOICES(models.TextChoices):
        PENDING = "P"
        ACCEPTED = "A"
        DENIED = "D"

    # requestor
    friend_r = models.ForeignKey(
        User,
        related_name="friendship_r_set",
        on_delete=models.CASCADE,
        verbose_name="Requestor",
    )
    # addressee
    friend_a = models.ForeignKey(
        User,
        related_name="friendship_a_set",
        on_delete=models.CASCADE,
        verbose_name="Addressee",
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING
    )

    def __str__(self):
        return f"{self.friend_r} - {self.friend_a} - {self.get_status_display()}"
