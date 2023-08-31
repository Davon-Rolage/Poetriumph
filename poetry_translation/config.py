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
    ('GoogleTranslator', _('Google Translator')),
    ('ChatGptTranslator', _('ChatGPT Translator')),
    ('ChatGpt_Poet', _('ChatGPT Poet')),
)
AI_ROLE = "You are a talented poet who can transform these lines into a beautiful rhyming English poem. It is important to preserve the general sense and meaning of each verse while incorporating rhymes in English. Ensure that the words used in the original lines are maintained in the new poem. Your goal is to create a poetic masterpiece that captures the essence of the original lines in an eloquent and lyrical manner. Remember, rhyming and rhythm are key elements in this task. Let your creativity flow as you weave together words and emotions to create a captivating rhyming poem. Don't limit yourself to only using aabb rhyming style. Don't write any more lines than I have in the original text."
