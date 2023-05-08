from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('images', views.images, name='images'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_images/', views.UploadedImagesByUserListView.as_view(), name='user_images'),
    path('generated_image/', views.generate_image, name='generate_image'),
    path('register/', views.register, name='register'),
]