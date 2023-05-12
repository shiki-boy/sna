from typing import Iterable, Optional
from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        if self.friend_a.uid == self.friend_r.uid:
            raise ValidationError(
                {"friend_a": "Cannot create a friend request to self"}
            )
        return super().clean()

    def __str__(self):
        return f"{self.friend_r} - {self.friend_a} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
