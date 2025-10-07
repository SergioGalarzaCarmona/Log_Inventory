from django.db import models
from Users.models import Profile
from django.contrib.auth.models import User
from Users.models import BaseAuditModel
from django.utils import timezone

class LiveChat(BaseAuditModel):
    admin_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_joined", blank=True)
    
    def __str__(self):
        return f"Chat entre {', '.join([user.username for user in self.users.all()])}"


class Message(models.Model):
    chat = models.ForeignKey(LiveChat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.user.username}: {self.text[:30]}"