from django.urls import path
from translator import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page
    path('translate/', views.translate, name='translate'),  # Handle translation requests
    path('download_mirror_result/', views.download_mirror_result, name='download_mirror_result')  # Download mirror Braille
]
