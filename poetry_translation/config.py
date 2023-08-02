SUPPORTED_LANGUAGES = (
    ('auto', 'определить язык'),
    ('english', "английский"),
    ('russian', 'русский'),
    ('spanish', "испанский"),
)
LANGUAGE_ENGINES = (
    ('GoogleTranslator', 'Google Translator'),
    ('ChatGptTranslator', 'ChatGPT Translator'),
    ('ChatGpt_Bot', 'ChatGPT Bot'),
)
AI_ROLE = 'You are a poet-polyglot who translates poems and pieces of art from {source_lang} to {target_lang} perfectly with precision and clarity using poetic language. Add nothing more but a translation written in {target_lang}. '
