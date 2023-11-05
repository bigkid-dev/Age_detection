from django.urls import path
from .views import (
    SignUpAPIView,
    LoginAPIView,
    ResetPassword
)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('reset-password', ResetPassword.as_view()),
]

