from django.urls import path

from .views import *


urlpatterns = [
    path('', TranslationFormView.as_view(), name='translation'),
    path('about/', AboutView.as_view(), name='about'),
    path('support-us/', SupportUsView.as_view(), name='support-us'),
    path('premium/', PremiumView.as_view(), name='premium'),
    path('poem-save/', SaveTranslation.as_view(), name='save_translation'),
    path('poems/', PoemListView.as_view(), name='poem_list'),
    path('poems/<int:pk>/', PoemDetailView.as_view(), name='poem_detail'),
    path('poems/update_translation/<int:poem_id>', UpdateTranslation.as_view(), name='update_translation'),
]
