from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:pk>/', views.room, name='room')
]

htmx_urlpatterns = [
    path('search-user/', views.search_user, name='search-user')
]

urlpatterns += htmx_urlpatterns
