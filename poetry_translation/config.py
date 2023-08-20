from django.utils.translation import gettext_lazy as _

SUPPORTED_LANGUAGES = (
    ('auto', _('Detect language')),
    ('english', _('English')),
    ('russian', _('Russian')),
    ('spanish', _('Spanish')),
    ('italian', _('Italian')),
    ('french', _('French')),
    ('german', _('German')),
    ('hindi', _('Hindi')),
    ('arabic', _('Arabic')),
    ('portuguese', _('Portuguese')),
    ('japanese', _('Japanese')),
    ('korean', _('Korean')),
    ('chinese (simplified)', _('Chinese Simplified')),
    ('chinese (traditional)', _('Chinese Traditional')),
    ('turkish', _('Turkish')),
    ('indonesian', _('Indonesian')),
)
LANGUAGE_ENGINES = (
    ('GoogleTranslator', 'Google Translator'),
    ('ChatGptTranslator', 'ChatGPT Translator'),
    ('ChatGpt_Poet', 'ChatGPT Poet'),
)
AI_ROLE = 'You are a poet-polyglot who translates poems and pieces of art from {source_lang} to {target_lang} perfectly with precision and clarity using poetic language. Add nothing more but a translation written in {target_lang}. '
