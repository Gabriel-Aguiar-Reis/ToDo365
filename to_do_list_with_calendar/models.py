from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Task(models.Model):
    """
    Template to represent a task.
    """

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        """
        Returns the sting representation of the task.
        """
        return f'{self.title} <{self.user}>'


class User(AbstractUser):
    """
    Template to represent a custom user with additional fields.
    """
    class Meta:
        db_table = 'auth_user'
    user_email = models.EmailField(blank=False)
    validated = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the string representation of the user.
        """
        return self.get_full_name()
