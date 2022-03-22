from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.testGet),
    path('books/', views.getBooks),
    path('groups/', views.getClubs)
]