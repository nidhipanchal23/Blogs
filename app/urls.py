from django.urls import path
from .views import UserRegistrationView, UserLoginView, VerifyOTP

urlpatterns = [
    # path('verify-uid-token/', VerifyUIDTokenView.as_view(), name='verify-uid-token'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('verify/', VerifyOTP.as_view()),
]