from django.db import models
from Users.models import Profile
from django.contrib.auth.models import User
from Users.models import BaseAuditModel


class LiveChat(BaseAuditModel):
    admin_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_joined", blank=True)
    
    def __str__(self):
        return f"Chat entre {', '.join([user.username for user in self.users.all()])}"


