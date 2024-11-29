
# Create your models here.
from django.db import models

class Usuario(models.Model):
    name = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.lastName}'

class Chat(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="chats")
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat de {self.user.name} - {self.timestamp}'