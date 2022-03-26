from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('modify/', views.modifyUser),
    path('info/', views.getInfo),
    path('groups/', views.getGroups),
    path('books/<str:list>/', views.getBooks),
    path('book/<str:isbn>/', csrf_exempt(views.BookList.as_view())),
]