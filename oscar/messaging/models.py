from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F('recipient')),
                name='%(app_label)s_%(class)s_sender_not_equal_recipient',
            )
        ]
