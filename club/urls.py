from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createGroup),
    path('info/<uuid:id>/', views.getClubInfo),
    path('join/<uuid:id>/', views.joinClub),
    path('delete/<uuid:id>/', views.deleteGroup),
    path('leave/<uuid:id>/', views.leaveClub),
    path('remove/<uuid:id>/', views.removeMember),
    path('book/<uuid:id>/', views.addBook),
    path('modify/<uuid:id>/', views.modifyGroup),

]