from django.urls import path
from . import views

urlpatterns = [
    # Home page showing posts
    path('', views.index, name='index'),

    # Post management
    path('add/', views.add_post, name='add_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/like/<int:pk>/', views.like_post, name='like_post'),

    # Comment management
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),

    # User authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # User profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    
    # Bookmarks
    path('post/<int:pk>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Discovery
    path('trending/', views.trending_posts, name='trending'),
    path('search/', views.search_enhanced, name='search_enhanced'),
]
