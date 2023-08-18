from django.urls import path

from .views import *


urlpatterns = [
    path('', TranslationFormView.as_view(), name='translation'),
    path('about/', AboutView.as_view(), name='about'),
    path('support-us/', SupportUsView.as_view(), name='support_us'),
    path('premium/', PremiumView.as_view(), name='premium'),
    path('poem-save/', SaveTranslation.as_view(), name='save_translation'),
    path('poems/', PoemListView.as_view(), name='poem_library'),
    path('poems/<int:pk>/', PoemDetailView.as_view(), name='poem_detail'),
    path('poems/update_translation/<int:poem_id>', UpdateTranslation.as_view(), name='update_translation'),
    path('poems/delete-translation/<int:poem_id>', DeleteTranslation.as_view(), name='delete_translation'),
    path('my-library/', MyLibraryView.as_view(), name='my_library'),
    path('get-premium/', GetPremiumView.as_view(), name='get_premium'),
    path('cancel-premium/', CancelPremiumView.as_view(), name='cancel_premium'),
    path('new-features/', NewFeaturesView.as_view(), name='new_features'),
]
