from django.db import models
from django.urls import reverse
from django.utils import timezone

from poetry_translation.config import LANGUAGE_ENGINES, SUPPORTED_LANGUAGES


class Poem(models.Model):
    class Meta:
        ordering = ('-pk',)

    title = models.CharField(max_length=50, default='Untitled')
    author = models.CharField(max_length=50, blank=True, default='')
    saved_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    original_text = models.TextField()
    translation = models.TextField()
    source_lang = models.CharField(choices=SUPPORTED_LANGUAGES, max_length=30)
    target_lang = models.CharField(choices=SUPPORTED_LANGUAGES, max_length=30)
    language_engine = models.CharField(choices=LANGUAGE_ENGINES, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_hidden = models.BooleanField(default=True)
    
    def __str__(self):
        if self.title == 'Untitled':
            return f'{self.pk} - {self.saved_by}'
        return self.title

    def get_absolute_url(self):
        return reverse('poem_detail', kwargs={'pk': self.pk})
    