from django.urls import path,include
from django.shortcuts import render

from . import views

app_name = 'material'

urlpatterns = [
    path('add_new/',views.add_new,name='add_new'),
    path('edit_m/<int:edit_id>/',views.edit_m,name='edit_m'),
    path('check/<int:check_id>/',views.check,name='check'),
    path('search_type/',views.search_type,name='search_type'),
    path('search_is_hospital/',views.search_is_hospital,name='search_is_hospital'),
    path('match/<int:m_id>/',views.match,name='match'),
    path('rematch/<int:m_id>/',views.rematch,name='rematch'),
    path('match_list/<int:user_id>/',views.match_list,name='match_list'),
]