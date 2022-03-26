from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.getBooks),
    path('groups/', views.getClubs),
    path('info/<str:isbn>/', views.getInfo)
]