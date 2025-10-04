from django.db import models
from Users.models import Profile
from django.contrib.auth.models import User


class LiveChat(models.Model):
    admin_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    requesting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="live_chat_requesting_user")
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="live_chat_requested_user")

    def __str__(self):
        return f"Chat de {self.admin_user.username} con {self.subuser.__str__}"
