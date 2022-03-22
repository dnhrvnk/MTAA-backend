from django.urls import path
from . import views

urlpatterns = [
    path('modify/', views.modifyUser),
    path('info/', views.getInfo),
    path('groups/', views.getGroups),
    path('books/', views.getBooks),
    path('book/', views.bookTolibrary),
    path('book/', views.bookFromLibrary)
]