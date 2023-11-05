from django.urls import path
from .views import SettingsView, Test, Homepage

urlpatterns = [
    path('test', SettingsView.as_view()),
    path('create-new-settings/', SettingsView.as_view()),
    path('test-code/', Test.as_view()),
    path('home', Homepage.as_view())
]