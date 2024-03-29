from django.utils.translation import gettext_lazy as _


AI_ROLE = """You are a talented poet who can transform these lines into a beautiful rhyming {language} poem.
It is important to preserve the general sense and meaning of each verse while incorporating rhymes in {language}.
Ensure that the words used in the original lines are preserved in the new poem.
Remember, rhyming and rhythm are key elements in this task.
Follow the rhyming pattern of the original text, but if it doesn't contain rhymes, then don't limit yourself to only using aabb rhyming style.
It is also important that you don't write any more lines than I have in the original text.
Your goal is to create a poetic masterpiece that captures the essence of the original lines in an eloquent and lyrical manner.
Let your creativity flow as you weave together words and emotions to create a captivating rhyming poem."""

CHARACTER_LIMIT = 800
CHARACTER_LIMIT_PREMIUM = 2000

LANGUAGE_ENGINES = [
    ('GoogleTranslator', _('Google Translator')),
    ('ChatGptTranslator', _('ChatGPT Translator')),
    ('ChatGpt_Poet', _('ChatGPT Poet')),
    ('MyMemoryTranslator', _('MyMemory Translator')),
]

SUPPORTED_LANGUAGES = [
    ('auto', _('Detect language')),
    ('english', _('English')),
    ('spanish', _('Spanish')),
    ('russian', _('Russian')),
    ('hindi', _('Hindi')),
    ('italian', _('Italian')),
    ('portuguese', _('Portuguese')),
    ('french', _('French')),
    ('german', _('German')),
    ('ukrainian', _('Ukrainian')),
    ('arabic', _('Arabic')),
    ('japanese', _('Japanese')),
    ('korean', _('Korean')),
    ('chinese (simplified)', _('Chinese Simplified')),
    ('chinese (traditional)', _('Chinese Traditional')),
    ('turkish', _('Turkish')),
    ('indonesian', _('Indonesian')),
]
