
from django.db import models


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Прочитана ли заявка
    is_read = models.BooleanField(default=False)

    # Статус заявки
    status = models.CharField(max_length=20, default="new")

    def __str__(self):
        return f"{self.name} - {self.phone}"
