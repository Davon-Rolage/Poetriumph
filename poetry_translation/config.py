SUPPORTED_LANGUAGES = (
    ('auto', 'Detect language'),
    ('english', 'English'),
    ('russian', 'Russian'),
    ('spanish', 'Spanish'),
    ('italian', 'Italian'),
    ('french', 'French'),
    ('german', 'German'),
    ('hindi', 'Hindi'),
    ('arabic', 'Arabic'),
    ('portuguese', 'Portuguese'),
    ('japanese', 'Japanese'),
    ('korean', 'Korean'),
    ('chinese (simplified)', 'Chinese Simplified'),
    ('chinese (traditional)', 'Chinese Traditional'),
    ('turkish', 'Turkish'),
    ('indonesian', 'Indonesian'),
)
LANGUAGE_ENGINES = (
    ('GoogleTranslator', 'Google Translator'),
    ('ChatGptTranslator', 'ChatGPT Translator'),
    ('ChatGpt_Poet', 'ChatGPT Poet'),
)
AI_ROLE = 'You are a poet-polyglot who translates poems and pieces of art from {source_lang} to {target_lang} perfectly with precision and clarity using poetic language. Add nothing more but a translation written in {target_lang}. '
