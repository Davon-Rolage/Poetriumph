from django.db import models
from django.utils import timezone

from poetry_translation.config import LANGUAGE_ENGINES, SUPPORTED_LANGUAGES


class Poem(models.Model):

    class Meta:
        ordering = ('-pk', )

    title = models.CharField(max_length=50, default='Untitled')
    user_text = models.TextField()
    text = models.TextField()
    source_lang = models.CharField(choices=SUPPORTED_LANGUAGES, max_length=30)
    target_lang = models.CharField(choices=SUPPORTED_LANGUAGES, max_length=30)
    language_engine = models.CharField(choices=LANGUAGE_ENGINES, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    
