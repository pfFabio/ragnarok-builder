from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_item, name='search_item'),
    path('build/save/', views.save_build, name='save_build'),
    path('build/list/', views.list_builds, name='list_builds'),
    path('build/load/<int:build_id>/', views.load_build, name='load_build'),
]