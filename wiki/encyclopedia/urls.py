from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("edit/<str:page_name>", views.edit, name="edit"),
    path("<str:page_name>", views.entry, name="entry")
    
]
