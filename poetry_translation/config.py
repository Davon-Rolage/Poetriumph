from django.utils.translation import gettext_lazy as _


AI_ROLE = "You are a talented poet who can transform these lines into a beautiful rhyming {language} poem. It is important to preserve the general sense and meaning of each verse while incorporating rhymes in {language}. Ensure that the words used in the original lines are preserved in the new poem. Remember, rhyming and rhythm are key elements in this task. Follow the rhyming pattern of the original text, but if it doesn't contain rhymes, then don't limit yourself to only using aabb rhyming style. It is also important that you don't write any more lines than I have in the original text. Your goal is to create a poetic masterpiece that captures the essence of the original lines in an eloquent and lyrical manner. Let your creativity flow as you weave together words and emotions to create a captivating rhyming poem."

CHARACTER_LIMIT = 800
CHARACTER_LIMIT_PREMIUM = 2000

LANGUAGE_ENGINES = [
    ('GoogleTranslator', _('Google Translator')),
    ('ChatGptTranslator', _('ChatGPT Translator')),
    ('ChatGpt_Poet', _('ChatGPT Poet')),
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


def get_gui_messages(keys_to_get: list) -> dict:
    gui_messages = dict()
    for key in keys_to_get:
        try:
            gui_messages.update(GUI_MESSAGES[key])
        except KeyError:
            pass
    return gui_messages


GUI_MESSAGES = {
    'accounts': {
        # Translators: this is a login title
        'login_title': _('Login'),
        # Translators: this is a login button
        'login_button': _('Login'),
        # Translators: this is a register title
        'register_title': _('Register'),
        # Translators: this is a register button
        'register_button': _('Register'),
        # Translators: this is an input form element
        'username': _('Username'),
        # Translators: this is an error message
        'username_taken': _('This username is already taken.'),
        # Translators: this is an input form element
        'password': _('Password'),
        # Translators: this is an input form element
        'password_repeat': _('Repeat Password'),
        # Translators: this is an input form element
        'password_forgot': _('Forgot Password?'),
        # Translators: this is an input form element
        'email': _('Email'),
        # Translators: this appears on the login page
        "do_not_have_account": _("Don't have an account?"),
        # Translators: this appears on the login page
        'register_now': _('Register Now!'),
        # Translators: this appears on the register page
        'already_have_account': _('Already have an account?'),
        # Translators: this appears on the register page
        'sign_in_now': _('Sign In Now!'),
        # Translators: this appears on the register page
        'registration_requirements': _('Registration requirements'),
        # Translators: this appears on the register page
        'registration_requirements_text': _("""<li>Only latin letters are allowed.</li>
<li>Username must contain only letters, digits and . + - _</li>
<li>Username must be at least 3 characters and no more than 15.</li>
<li>Your password can't be too similar to your other personal information.</li>
<li>Your password must contain at least 8 characters.</li>
<li>Your password can't be a commonly used password.</li>
<li>Your password can't be entirely numeric.</li>"""
        )
    },
    'base': {
        # Translators: this is a navbar item
        'poem_translation': _('Poem Translation'),
        # Translators: this is a navbar item
        'poem_library': _('Poem Library'),
        # Translators: this is a navbar item
        'my_library': _('My Library'),
        # Translators: this is a navbar item
        'about': _('About'),
        # Translators: this is a navbar item
        'support_us': _('Support Us'),
        # Translators: this is a navbar item
        'premium': _('Premium'),
        # Translators: this appears in the navbar
        'greetings': _('Hi'),
        # Translators: this is a navbar item
        'profile': _('My Profile'),
        # Translators: this is a navbar item
        'logout': _('Log out'),
        # Translators: this is a navbar item
        'admin_panel': _('Admin'),
        # Translators: this is a navbar item
        'login': _('Login'),
        # Translators: this is a navbar item
        'register': _('Register'),
    },
    'index': {
        # Translators: this is the title of the index page
        'index_title': _('Poem Translation'),
        # Translators: this is the description of the index page
        'index_description': _('Insert your poem and choose translation engine.'),
        # Translators: this is a translate button text
        'button_translate_text': _('Translate'),
        # Translators: this is a translate button loading text
        'button_loading_text': _('Translating'),
        # Translators: this is a download button text
        'button_download_text': _('Download'),
        # Translators: this is a "save to library" button text
        'button_save_to_library': _('Save to library'),
        # Translators: this is a placeholder for the input textarea
        'placeholder_original_text': _('Insert your poem...'),
        # Translators: this is a placeholder for the translation textarea
        'placeholder_translation': _('Your translation will be here...'),
    },
    'profile': {
        # Translators: this is a profile page title
        'welcome': _('Welcome'),
        # Translators: this is a profile settings option
        'home': _('Home'),
        # Translators: this is a profile settings option
        'profile': _('Profile'),
        # Translators: this is a profile settings option
        'settings': _('Settings'),
        # Translators: this is a profile settings option
        'achievements': _('Achievements'),
        # Translators: this is profile info
        'total_poems': _('Total number of poems:'),
        # Translators: this is profile info
        'date_joined': _('Date joined'),
        # Translators: this is profile info
        'has_premium': _('You have premium status'),
        # Translators: this is profile info
        'no_premium': _('You have free status.'),
        # Translators: this is profile info. Goes after 'You have free status'
        'upgrade_to_premium': _('Upgrade to premium'),
        # Translators: this is a profile settings option (button)
        'delete_account': _('Delete account'),
        # Translators: this is a confirmation text for the delete account
        'delete_account_confirm': _('Are you sure you want to delete your account?'),
        # Translators: this is an achievement text
        'never_give_up': _('Never give up!'),
        # Translators: this is an achievement text
        'have_1_poem': _('Save your first poem to the library!'),
        # Translators: this is an achievement text
        'have_n_poems': _('Poems in the library:'),
    },
    'about': {
        'about_poetriumph': _('About Poetriumph'),
        'about_poetriumph_text': _('Poetriumph is a project that allows users to translate poetry from one language to another. It is designed to provide a user-friendly platform for enhancing translation skills and exploring poetry from different cultures.'),
        'source_code': _('Source code is available on GitHub'),
    },
    'tooltips': {
        'save_to_library': _('Sign in to save to library!'),
        'loading_text_chatgpt': _('ChatGPT response may take up to 2 minutes'), 
        'google_translator': _("Literal translation with Google Translator"),
        'chatgpt_translator': _("Take the context into account and use the power of AI to translate your text"),
        'chatgpt_poet': _("Make a rhyming poem (only English and Spanish) out of your text, preserving rhythm and rhyming patterns.\nOr make a poem using just a prompt, like `I'm happy that you're with me`"),
    },
    'forms': {
        # Translators: this is a form placeholder
        'placeholder_title': _('Title...'),
        # Translators: this is a form placeholder
        'placeholder_author': _('Author...'),
        # Translators: this is a form placeholder
        'placeholder_original_text': _('Original Text...'),
        # Translators: this is a form placeholder
        'placeholder_translation_text': _('Translation text...'),
        
        'error_captcha': _('You must pass the reCAPTCHA test'),
        'error_username_required': _('Username is required'),
        'error_username_contains_spaces': _('Username cannot contain spaces'),
        'error_username_invalid_chars': _('Username contains invalid characters'),
        'error_username_min_length': _('Username is too short'),
        'error_username_max_length': _('Username is too long'),
        'error_email_invalid': _('Email is invalid'),
        'error_password_min_length': _('Password is too short'),
        'error_invalid_credentials': _('Invalid username or password'),
    },
    'messages': {
        'poem_updated': _('The poem has been successfully updated'),
        'poem_deleted': _('The poem has been successfully deleted'),
        'badge_earned': _('You have earned a badge! Check out your profile!'),
        'user_deleted': _('The user has been successfully deleted'),
        'email_subject': _('Confirm your account on Poetriumph'),
        'email_sent': _('<b>{user}</b>, please check your email <b>{to_email}</b> to activate your account.'),
        'activation_successful': _('Thank you for confirming your email. You can now sign in to your account.'),
    },
    'error_messages': {
        'email_sent': _('Problem sending email to <b>{to_email}</b>, please try again.'),
        'activation_failed': _('Activation link is invalid! Please try again.'),
        'poem_update': _('Please fill out all the required fields.'),
    },
    'table_columns': {
        # Translators: this is a table id header
        'poem_counter': _('#'),
        # Translators: this is a table title header
        'poem_title': _('Title'),
        # Translators: this is a table author header
        'poem_author': _('Author'),
        # Translators: this is a table "target language" header
        'poem_target_language': _('Target Language'),
        # Translators: this is a table "saved by" header
        'poem_saved_by': _('Saved by'),
        # Translators: this is a table "update at" header
        'poem_updated_at': _('Updated at'),
        # Translators: this is a table "is hidden" header
        'poem_is_hidden': _('Is hidden'),
        # Translators: this is a "Hidden" poem badge
        'hidden_state': _('Hidden'),
    },
    'poem_library': {
        # Translators: this is the title of the "Poem Library" page
        'poem_library_title': _('Poem Library'),
    },
    'poem_my_library': {
        # Translators: this is the title of the "My Library" page
        'my_library_title': _('My Library'),    
    },
    'poem_detail': {
        # Translators: this appears if a poem is hidden
        'poem_hidden': _('This poem is hidden by its author'),
        # Translators: this is a poem detail label
        'language_engine': _('Translation Engine'),
        # Translators: this is a "Change Poem" button
        'button_change_poem': _('Change Poem'),
        # Translators: this is a poem detail label
        'poem_title': _('Title:'),
        # Translators: this is a poem detail label
        'poem_author': _('Author:'),
        # Translators: this is a poem detail label
        'poem_saved_by': _('Saved by'),
        # Translators: this is a poem detail label
        'checkbox_hide_from_library': _('Hide from Poem Library'),
        # Translators: this is a badge that appears when a poem is hidden
        'poem_hidden_badge': _('Poem hidden'),
        # Translators: this is a poem detail label
        'original_text': _('Original Text'),
        # Translators: this is a poem detail label
        'translation_text': _('Translation'),
    },
    'poem_update': {
        'not_allowed': _('You are not allowed to edit this poem.'),
        # Translators: this is a "Delete Poem" button
        'button_delete_poem': _('Delete'),
        'confirm_poem_delete': _('Are you sure you want to delete this poem?'),
        # Translators: this is a "Save Changes" button
        'button_save_changes': _('Save Changes'),
        # Translators: this is a "Poem Update" label
        'poem_updated_at': _('Updated at'),
    },
    'support_us': {
        # Translators: this is the title of the "Support Us" page
        'support_us_title': _('Support Us'),
        'download_bg_image': _('Download this background image'),
    },
    'premium': {
        'not_authenticated': _('Premium is only available for registered users. Sign in and try again.'),
        # Translators: this is the title of the "Premium" page
        'premium_title': _('Premium'),
        'premium_description': _('Get access to the following premium features:'),
        'premium_features': _('''<li>Premium users can translate poetry into more languages</li>
<li>Character limit is increased to 2000 characters</li>
<li>You get your own premium badge on your profile</li>
<li>You will be able to earn badges for saving poems</li>'''),
        # Translators: this is a "Get Premium" button
        'button_get_premium': _('Try out for free!'),
        'thank_you_premium': _('Thank you for upgrading to premium!<br>Enjoy all the features we have to offer!'),
        # Translators: this is a "Cancel Premium" button
        'button_cancel_premium': _('Cancel Premium'),
    },
}
