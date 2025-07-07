from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class JournalEntry(models.Model):
    input_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # saves the time of object creation only
    