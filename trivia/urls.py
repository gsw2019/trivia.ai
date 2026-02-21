from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("game_page/", views.game_page, name="game_page"),
]