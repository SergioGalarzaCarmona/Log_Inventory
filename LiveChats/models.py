from django.db import models
from Users.models import Profile, Subprofile


class LiveChat(models.Model):
    admin_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subuser = models.ForeignKey(Subprofile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat de {self.admin_user.username} con {self.subuser.__str__}"
