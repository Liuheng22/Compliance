from django.urls import path
from . import views

app_name = 'dataapp'

urlpatterns=[
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('post_list/', views.post_list, name="post_list"),
    path('post_list/<int:pk>/', views.post_delete, name='post_delete'),
    path('post_list/<slug:post>/', views.post_detail, name='post_detail'),
    path('post_list/<slug:post>/handle_high_level/', views.handle_high_level, name='handle_high_level'),
    path('post_list/<slug:post>/generate_report/',views.generate_report,name='generate_report'),
    path('new_post/', views.MainView.as_view(), name="upload-view"),
    path('new_post/upload/', views.file_upload_view, name="upload_view"),
    path('testtext/dlp/',views.dlptext,name='dlp'),
    ]
