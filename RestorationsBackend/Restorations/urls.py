from django.urls import path
from Restorations.views import *

app_name = 'Restorations'
urlpatterns = [
    path('<int:restore_id>/', card_view,  name='card'),
    path('', cards_view, name='cards'),
]

