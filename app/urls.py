from django.urls import path
from .views import EmployeeDataView, TaskCreateView, UserRegistrationView, UserLoginView

urlpatterns = [
    # path('verify-uid-token/', VerifyUIDTokenView.as_view(), name='verify-uid-token'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('createtask/', TaskCreateView.as_view()),
    path('employee/', EmployeeDataView.as_view()),
    # path('user-details/', UserView.as_view()),
]