# api/urls.py

from django.urls import path
from .views import post_view, lll_views

urlpatterns = [
    path('user/posts/', post_view.PostList.as_view(), name='post-list'),
    path('user/posts/<int:pk>/', post_view.PostDetail.as_view(), name='post-detail'),
    path('user/posts/top_ten/', post_view.TopTenPostListAPIView.as_view(), name='top-ten-posts'),  # Update this line
    path('register', lll_views.RegisterView.as_view()),
    path('login', lll_views.LoginView.as_view()),
    path('user', lll_views.UserView.as_view()),
    path('logout', lll_views.LogoutView.as_view()),
]