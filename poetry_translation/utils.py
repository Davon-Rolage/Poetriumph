import openai
from deep_translator import (ChatGptTranslator, GoogleTranslator,
                             MyMemoryTranslator)
from django.http import HttpResponse
from openai.error import *

from .config import AI_ROLE


def translate(language_engine, source_lang, target_lang, original_text, proxies=None):
    lang_engine_map = {
        "GoogleTranslator": GoogleTranslator,
        "ChatGptTranslator": ChatGptTranslator,
        "MyMemoryTranslator": MyMemoryTranslator,
    }
    language_engine = lang_engine_map[language_engine]
    translator = language_engine(
        api_key=openai.api_key,
        source=source_lang,
        target=target_lang,
        proxies=proxies
    )
    try:
        translated = translator.translate(original_text)
        return translated
    
    except Exception as e: # pragma: no cover
        return HttpResponse(str(e))


def translate_gpt(original_text, language, character_limit) -> (str | HttpResponse): # pragma: no cover
    max_tokens = int(character_limit / 5)
    ai_role = AI_ROLE.format(language=language)
    try:
        completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role':'system', 'content':ai_role}, 
            {'role':'user', 'content':original_text},
        ],
        max_tokens=max_tokens
    )
    except Exception as e:
        return str(e)
    
    answer = completion.choices[0].message.content
    return answer
