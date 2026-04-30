"""
URL configuration for evaluaciones_total_grades_estudiantes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from calificaciones_total_grades_estudiantes.views import (
    DashboardRedirectView,
    EstudianteDashboardView,
    HomeView,
    ProfesorDashboardView,
    RoleLoginView,
    SuperadminDashboardView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', RoleLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('panel/', DashboardRedirectView.as_view(), name='dashboard'),
    path('panel/superadmin/', SuperadminDashboardView.as_view(), name='superadmin_dashboard'),
    path('panel/profesor/', ProfesorDashboardView.as_view(), name='profesor_dashboard'),
    path('panel/estudiante/', EstudianteDashboardView.as_view(), name='estudiante_dashboard'),
    path('admin/', admin.site.urls),
    path('calificaciones/', include('calificaciones_total_grades_estudiantes.urls')),
]