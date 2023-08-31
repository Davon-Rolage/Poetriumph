from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _

from poetry_translation.config import LANGUAGE_ENGINES, SUPPORTED_LANGUAGES

from .models import Poem


class PoemDetailForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
        
    source_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES, widget=forms.Select(
        attrs={
            'disabled': True,
            'style': 'flex: 1; width: 200px;', 
            'class': 'form-select', 
            'aria-select': 'Source Language'
        }
    ))
    target_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES[1:], widget=forms.Select(
        attrs={
            'disabled': True,
            'style': 'flex: 1; width: 200px;', 
            'class': 'form-select', 
            'aria-select': 'Target Language'
        }
    ))
    language_engine = forms.ChoiceField(choices=LANGUAGE_ENGINES, widget=forms.Select(
        attrs={
            'readonly': True,
            'style': 'flex: 1; width: 200px;', 
            'class': 'form-select', 
            'aria-select': 'Language Engine'
        }
    ))
    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'readonly': 'true',
            'id': 'title',
            'name': 'title',
            'class': 'form-control',
            'placeholder': _('Title...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    author = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'readonly': 'true',
            'id': 'author',
            'name': 'author',
            'class': 'form-control',
            'placeholder': _('Author...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    saved_by = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'default': 'Anonymous',
            'readonly': True,
            'id': 'saved_by',
            'name': 'saved_by',
            'class': 'form-control',
            'placeholder': _('Saved by...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    is_hidden = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'disabled': True,
            'id': 'flexSwitchCheckDefault',
            'name': 'is_hidden',
            'class': 'form-check-input',
        }
    ))
    original_text = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'original_text',
            'class': 'message_text',
            'style': 'margin-top: 10px;',
            'placeholder': _('Original text...'),
        }
    ))
    translation = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'translation_text',
            'class': 'message_text',
            'style': 'margin-top: 10px;',
            'placeholder': _('Translation text...'),
        }
    ))
    updated_at = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        attrs={
            'readonly': True,
            'id': 'updated_at',
            'name': 'updated_at',
            'auto_now': True
        }
    ))


class PoemUpdateForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
        
    source_lang = forms.ChoiceField(required=False, choices=SUPPORTED_LANGUAGES, widget=forms.Select(
        attrs={
            'style': 'flex: 1; width: 200px;', 
            'class': 'form-select', 
            'aria-select': 'Source Language'
        }
    ))
    target_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES[1:], widget=forms.Select(
        attrs={
            'style': 'flex: 1; width: 200px;', 
            'class': 'form-select', 
            'aria-select': 'Target Language'
        }
    ))
    language_engine = forms.ChoiceField(choices=LANGUAGE_ENGINES, widget=forms.Select(
        attrs={
            'style': 'flex: 1; width: 200px; padding-left: 12px;', 
            'class': 'form-select', 
            'aria-select': 'Language Engine'
        }
    ))
    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'id': 'title',
            'name': 'title',
            'class': 'form-control',
            'placeholder': _('Title...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    author = forms.CharField(required=False, max_length=50, widget=forms.TextInput(
        attrs={
            'id': 'author',
            'name': 'author',
            'class': 'form-control',
            'placeholder': _('Author...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    saved_by = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'readonly': True,
            'default': 'Anonymous',
            'id': 'saved_by',
            'name': 'saved_by',
            'class': 'form-control',
            'placeholder': _('Saved by...'),
            'style': 'width: 300px; padding-left: 15px;',
        }
    ))
    is_hidden = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'id': 'flexSwitchCheckDefault',
            'name': 'is_hidden',
            'class': 'form-check-input',
        }
    ))
    original_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'original_text',
            'class': 'message_text',
            'style': 'margin-top: 10px;',
            'placeholder': _('Original text...'),
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'translation',
            'class': 'message_text',
            'style': 'margin-top: 10px;',
            'placeholder': _('Translation text...'),
        }
    ))
    updated_at = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'readonly': True,
            'id': 'updated_at',
            'name': 'updated_at',
            'class': 'form-control',
            'style': 'max-width: 170px;',
        }
    ))
    
    def save(self):
        poem = super().save(commit=False)
        poem.updated_at = timezone.now()
        poem.save()
        return poem
