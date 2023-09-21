from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    fullname = models.CharField(max_length=255, verbose_name='Full Name')
    subject = models.CharField(max_length=255, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return f"{self.fullname} - {self.subject}"

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']
