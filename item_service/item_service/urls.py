from django.contrib import admin
from django.urls import path
from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search_item, name='search_item'),
]
