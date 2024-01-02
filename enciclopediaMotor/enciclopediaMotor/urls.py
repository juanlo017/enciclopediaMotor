"""
URL configuration for enciclopediaMotor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),   
    path('scrapear/', views.scrap_data),
    path('cargar/', views.load_db),
    path('cargar_whoosh/', views.load_whoosh),
    path('buscar_nombre_descripcion/', views.search_whoosh_title_description),
    path('buscar_por_tipo/', views.search_whoosh_type),
]
