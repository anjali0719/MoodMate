from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class JournalEntry(models.Model):
    input_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # saves the time of object creation only
    journal_title = models.CharField(max_length=50, default='Untitled Journal')
    response_text = models.TextField()
    
    def __str__(self):
        return f"{self.journal_title}"

    class Meta:
        ordering = ['-created_at']

