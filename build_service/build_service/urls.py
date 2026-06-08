from django.contrib import admin
from django.urls import path
from builds import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list_builds, name='list_builds'),
    path('save/', views.save_build, name='save_build'),
    path('<int:build_id>/', views.load_build, name='load_build'),
]
