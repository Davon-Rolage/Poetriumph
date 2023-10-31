from django.utils.translation import gettext_lazy as _


AI_ROLE = "You are a talented poet who can transform these lines into a beautiful rhyming {language} poem. It is important to preserve the general sense and meaning of each verse while incorporating rhymes in {language}. Ensure that the words used in the original lines are preserved in the new poem. Remember, rhyming and rhythm are key elements in this task. Follow the rhyming pattern of the original text, but if it doesn't contain rhymes, then don't limit yourself to only using aabb rhyming style. It is also important that you don't write any more lines than I have in the original text. Your goal is to create a poetic masterpiece that captures the essence of the original lines in an eloquent and lyrical manner. Let your creativity flow as you weave together words and emotions to create a captivating rhyming poem."

CHARACTER_LIMIT = 800
CHARACTER_LIMIT_PREMIUM = 2000

LANGUAGE_ENGINES = (
    ('GoogleTranslator', _('Google Translator')),
    ('ChatGptTranslator', _('ChatGPT Translator')),
    ('ChatGpt_Poet', _('ChatGPT Poet')),
)
LANGUAGE_ENGINE_TOOLTIPS = {
    'GoogleTranslator': _("Literal translation with Google Translator"),
    'ChatGptTranslator': _("Take the context into account and use the power of AI to translate your text"),
    'ChatGpt_Poet': _("Make a rhyming poem (only English and Spanish) out of your text, preserving rhythm and rhyming patterns.\nOr make a poem using just a prompt, like `I'm happy that you're with me`"),
}

SUPPORTED_LANGUAGES = (
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
)

GUI_MESSAGES = {
    'forms': {
        'placeholder_title': _('Title...'),
        'placeholder_author': _('Author...'),
        'placeholder_original_text': _('Original Text...'),
        'placeholder_translation_text': _('Translation text...'),
        
        'error_captcha': _('You must pass the reCAPTCHA test'),
        'error_username_contains_spaces': _('Username cannot contain spaces'),
        'error_username_contains_invalid_chars': _('Username contains invalid characters'),
        'error_username_too_short': _('Username is too short'),
        'error_username_too_long': _('Username is too long'),
        'error_invalid_email': _('Email contains invalid characters'),
        'error_password_too_short': _('Password is too short'),
        'error_passwords_do_not_match': _('Passwords do not match'),
        'error_invalid_credentials': _('Invalid username or password'),
    },
    'messages': {
        'poem_updated': _('The poem has been successfully updated'),
        'poem_deleted': _('The poem has been successfully deleted'),
        'badge_earned': _('You have earned a badge! Check out your profile!'),
        'user_deleted': _('The user has been successfully deleted'),
        'email_subject': _('Confirm your account on Poetriumph'),
        'email_sent': _('<b>{user}</b>, please check your email <b>{to_email}</b> to activate your account.'),
        'activation_successful': _('Thank you for confirming your email. You can now log in to your account.')
    },
    'error_messages': {
        'email_sent': _('Problem sending email to <b>{to_email}</b>, please try again.'),
        'activation_failed': _('Activation link is invalid! Please try again.'),
    },
    'loading_button_text': _('Translating'),
    'loading_tooltip_text': _('ChatGPT response may take up to 2 minutes'), 
}
