import os
import openai
from .config import AI_ROLE
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection,
                             exceptions)
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

def translate(language_engine, source_lang, target_lang, user_prompt, proxies):
    lang_engine_map = {
        "GoogleTranslator": GoogleTranslator,
        "ChatGptTranslator": ChatGptTranslator,
        # "DeeplTranslator": DeeplTranslator,
    }
    language_engine = lang_engine_map[language_engine]
    translator = language_engine(
        api_key=openai.api_key,
        source=source_lang,
        target=target_lang,
        proxies=proxies
    )
    translated = translator.translate(user_prompt)
    return translated if language_engine != ChatGptTranslator else translated.strip('"')


def translate_gpt(source_lang, target_lang, user_prompt):
    ai_role = AI_ROLE.format(source_lang=source_lang, target_lang=target_lang)
    completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role':'system', 'content':ai_role}, 
        {'role':'user', 'content':user_prompt},
    ]
)
    answer = completion.choices[0].message.content
    return answer

