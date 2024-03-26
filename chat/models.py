from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.author.username}: {self.timestamp}: {self.content}'

    @staticmethod
    def get_last_10_messages():
        messages = Message.objects.order_by('-timestamp')[:10]
        return messages
    
