from django.db import models


class CodeSnippet(models.Model):
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
