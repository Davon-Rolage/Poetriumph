from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _

from poetry_translation.config import LANGUAGE_ENGINES, SUPPORTED_LANGUAGES

from .config import GUI_MESSAGES
from .models import Poem


class ComposePoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'        
    
    source_lang = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-select',
            'aria-select': 'Source Language',
        },
    ))
    target_lang = forms.ChoiceField(widget=forms.Select(
        attrs={
            'id': 'target-language-dropdown',
            'class': 'form-select',
            'aria-select': 'Target Language'}))
    language_engine = forms.ChoiceField(widget=forms.Select(
        attrs={
            'id': 'language-engine-dropdown',
            'class': 'form-select',
            'aria-select': 'Translation Service'}))
    original_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['index']['placeholder_original_text'], 
            'rows': '10', 
            'id': 'original-text', 
            'name': 'original_text'
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'poem-textarea translation_text text-to-copy',
            'placeholder': GUI_MESSAGES['index']['placeholder_translation'], 
            'rows': '10', 
            'id': 'translation-text', 
            'name': 'translation'
        }
    ))
    
    def __init__(self, *args, **kwargs):
        kwargs = kwargs.pop('initial')
        source_languages = kwargs.pop('source_languages', None)
        target_languages = kwargs.pop('target_languages', None)
        language_engines = kwargs.pop('language_engines', None)
        super().__init__(*args, **kwargs)
        self.fields['source_lang'].choices = source_languages
        self.fields['target_lang'].choices = target_languages
        self.fields['language_engine'].choices = language_engines


class PoemDetailForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
        exclude = ['saved_by']
        
    source_lang = forms.ChoiceField(disabled=True, choices=SUPPORTED_LANGUAGES, widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Source Language'
        }
    ))
    target_lang = forms.ChoiceField(disabled=True, choices=SUPPORTED_LANGUAGES[1:], widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Target Language'
        }
    ))
    language_engine = forms.ChoiceField(disabled=True, choices=LANGUAGE_ENGINES, widget=forms.Select(
        attrs={
            'class': 'form-select', 
            'aria-select': 'Language Engine'
        }
    ))
    title = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={
            'id': 'title',
            'name': 'title',
            'class': 'form-control',
            'placeholder': GUI_MESSAGES['forms']['placeholder_title'],
        }
    ))
    author = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={
            'id': 'author',
            'name': 'author',
            'class': 'form-control',
            'placeholder': GUI_MESSAGES['forms']['placeholder_author'],
        }
    ))
    original_text = forms.CharField(disabled=True, widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'original_text',
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_original_text'],
        }
    ))
    translation = forms.CharField(disabled=True, widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'translation_text',
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_translation_text'],
        }
    ))


class PoemUpdateForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
        exclude = ['saved_by']
        
    source_lang = forms.ChoiceField(choices=SUPPORTED_LANGUAGES, widget=forms.Select(
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
        }),
        error_messages={
            'required': GUI_MESSAGES['forms']['error_title_required'],
        }
    )
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
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_original_text'],
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 10,
            'name': 'translation',
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_translation_text'],
        }
    ))
    updated_at = forms.DateTimeField(disabled=True, widget=forms.DateTimeInput(
        attrs={
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
