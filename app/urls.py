from django.urls import path
from .views import BlogView, PublishedBlogs, UserRegistrationView, UserLoginView, VerifyOTP

urlpatterns = [
    # path('verify-uid-token/', VerifyUIDTokenView.as_view(), name='verify-uid-token'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('home/', PublishedBlogs.as_view()),
    path('edit-blog/',BlogView.as_view()),
    path('blog-list/',BlogView.as_view()),
    path('edit-blog/<int:blog_id>/',BlogView.as_view()),
    path('delete-blog/<int:blog_id>/',BlogView.as_view()),
    

]

# path('<str:username>/', BlogView.as_view()),
#     path('<str:username>/blogs/', BlogView.as_view()),
#     path('<str:username>/blogs/<int:blog_id>/', BlogView.as_view()),
#     path('<str:username>/blogs/update/<int:blog_id>/', BlogView.as_view()),