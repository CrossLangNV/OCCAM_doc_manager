from django.db import models


class UserTutorial(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    has_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
