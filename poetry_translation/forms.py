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
    original_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'original_text',
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_original_text'],
        }
    ))
    translation = forms.CharField(widget=forms.Textarea(
        attrs={
            'readonly': True,
            'rows': 10,
            'name': 'translation_text',
            'class': 'poem-textarea text-to-copy',
            'placeholder': GUI_MESSAGES['forms']['placeholder_translation_text'],
        }
    ))
    
    def __init__(self, *args, **kwargs):
        source_lang = kwargs.pop('source_lang', None)
        target_lang = kwargs.pop('target_lang', None)
        language_engine = kwargs.pop('language_engine', None)
        title = kwargs.pop('title', None)
        author = kwargs.pop('author', None)
        original_text = kwargs.pop('original_text', None)
        translation = kwargs.pop('translation', None)
        super().__init__(*args, **kwargs)
        
        self.fields['source_lang'].initial = source_lang
        self.fields['target_lang'].initial = target_lang
        self.fields['language_engine'].initial = language_engine
        self.fields['title'].initial = title
        self.fields['author'].initial = author
        self.fields['original_text'].initial = original_text
        self.fields['translation'].initial = translation


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
    updated_at = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'readonly': True,
            'id': 'updated_at',
            'name': 'updated_at',
            'class': 'form-control',
        }
    ))
    
    def __init__(self, *args, **kwargs):
        source_lang = kwargs.get('source_lang')
        target_lang = kwargs.get('target_lang')
        language_engine = kwargs.get('language_engine')
        title = kwargs.get('title')
        author = kwargs.get('author')
        is_hidden = kwargs.get('is_hidden')
        original_text = kwargs.get('original_text')
        translation = kwargs.get('translation')
        updated_at = kwargs.get('updated_at')
        super().__init__(*args, **kwargs)
        self.fields['source_lang'].initial = source_lang
        self.fields['target_lang'].initial = target_lang
        self.fields['language_engine'].initial = language_engine
        self.fields['title'].initial = title
        self.fields['author'].initial = author
        self.fields['is_hidden'].initial = is_hidden
        self.fields['original_text'].initial = original_text
        self.fields['translation'].initial = translation
        self.fields['updated_at'].initial = updated_at
    
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
