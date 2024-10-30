from django.urls import path
from . import views

app_name = 'starwars'
urlpatterns = [
    path('sync/', view=views.starwars_sync_view, name='sync'),
    path('async/', view=views.starwars_async_view, name='async'),
]
