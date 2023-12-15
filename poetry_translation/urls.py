from django.urls import path

from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='translation'),
    path('about/', AboutView.as_view(), name='about'),
    path('support-us/', SupportUsView.as_view(), name='support_us'),
    path('poem-translate/', GetTranslation.as_view(), name='get_translation'),
    path('poem-save/', SaveTranslation.as_view(), name='save_translation'),
    path('poems/', PoemLibraryListView.as_view(), name='poem_library'),
    path('poems/<int:pk>/', PoemDetailView.as_view(), name='poem_detail'),
    path('poems/<int:pk>/update/', PoemUpdateView.as_view(), name='poem_update'),
    path('poems/<int:pk>/update/poem-delete', PoemDeleteView.as_view(), name='poem_delete'),
    path('my-library/', MyLibraryListView.as_view(), name='my_library'),
    path('new-features/', NewFeaturesView.as_view(), name='new_features'),
    path('test/', TestView.as_view(), name='test'),
]
