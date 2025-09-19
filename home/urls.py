from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_post, name='add_post'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/like/<int:pk>/', views.like_post, name='like_post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'), # New line for deleting comments
]