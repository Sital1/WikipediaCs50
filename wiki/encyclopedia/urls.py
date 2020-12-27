from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<str:name>',views.entry,name="entry"),
    path('newpage',views.newpage,name="newpage"),
    path('wiki/<str:name>/edit',views.edit,name="edit"),
    path('randomPage',views.randomPage,name = "randomPage"),
    path('search', views.search, name="search"),
    
]
