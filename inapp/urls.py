from django.urls import path
from . import views
urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('search/', views.tweet_search, name='tweet_search'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/tweet/<int:pk>/', views.tweet_detail_admin, name='tweet_detail_admin'),
    path('admin_dashboard/tweet/<int:pk>/delete/', views.tweet_delete_admin, name='tweet_delete_admin'),
    path('admin/bulk_action/', views.tweet_bulk_action, name='tweet_bulk_action'),
    path('admin/tweet/<int:tweet_id>/toggle_flag/', views.tweet_toggle_flag, name='tweet_toggle_flag'),
    path('admin/tweet/<int:tweet_id>/edit/', views.tweet_admin, name='tweet_edit_admin'),  # <--- Add this line
]
