from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _

from poetry_translation.config import LANGUAGE_ENGINES, SUPPORTED_LANGUAGES

from .config import GUI_MESSAGES
from .models import Poem


class PoemDetailForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
        exclude = ['saved_by']
        
    source_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES, widget=forms.Select(
        attrs={
            'disabled': True,
            'class': 'form-select', 
            'aria-select': 'Source Language'
        }
    ))
    target_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES[1:], widget=forms.Select(
        attrs={
            'disabled': True,
            'class': 'form-select', 
            'aria-select': 'Target Language'
        }
    ))
    language_engine = forms.ChoiceField(choices=LANGUAGE_ENGINES, widget=forms.Select(
        attrs={
            'readonly': True,
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
            'placeholder': GUI_MESSAGES['forms']['placeholder_title'],
        }
    ))
    author = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'readonly': 'true',
            'id': 'author',
            'name': 'author',
            'class': 'form-control',
            'placeholder': GUI_MESSAGES['forms']['placeholder_author'],
        }
    ))
    is_hidden = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'disabled': True,
            'id': 'flexSwitchCheckDefault',
            'name': 'is_hidden',
        }
    ))
    original_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'original_text',
            'class': 'message_text text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_original_text'],
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'translation_text',
            'class': 'message_text text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_translation_text'],
        }
    ))
    updated_at = forms.DateTimeField(widget=forms.DateTimeInput(
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
        exclude = ['saved_by']
        
    source_lang = forms.ChoiceField(required=False, choices=SUPPORTED_LANGUAGES, widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Source Language',
        }
    ))
    target_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES[1:], widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Target Language'
        }
    ))
    language_engine = forms.ChoiceField(choices=LANGUAGE_ENGINES, widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Language Engine'
        }
    ))
    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'id': 'title',
            'name': 'title',
            'class': 'form-control',
            'placeholder': GUI_MESSAGES['forms']['placeholder_title'],
        }
    ))
    author = forms.CharField(required=False, max_length=50, widget=forms.TextInput(
        attrs={
            'id': 'author',
            'name': 'author',
            'class': 'form-control',
            'placeholder': GUI_MESSAGES['forms']['placeholder_author'],
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
            'class': 'message_text text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_original_text'],
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'translation',
            'class': 'message_text text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_translation_text'],
        }
    ))
    updated_at = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'readonly': True,
            'id': 'updated_at',
            'name': 'updated_at',
            'class': 'form-control',
        }
    ))
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if not title:
            self.fields['title'].widget.attrs.update({'class': 'form-control border-danger'})

        return cleaned_data
    
    def save(self):
        poem = super().save(commit=False)
        poem.updated_at = timezone.now()
        poem.save()
        return poem
