from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatSession(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.title}"

    class Meta:
        ordering = ['-created_at']

class JournalEntry(models.Model):
    input_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # saves the time of object creation only
    response_text = models.TextField()
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='entries')
    
    def __str__(self):
        return f"{self.input_text[:10]}"

    class Meta:
        ordering = ['-created_at']

# everytime users opens a chat window, get the chat_session.id based on it filter the JournalEntry objects. If there is no chat_session, create a new one.
# If there is a chat_session, create a new JournalEntry with the chat_session.id.