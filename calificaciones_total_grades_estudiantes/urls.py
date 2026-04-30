from django.urls import path

from .views import (
    CalificacionCreateView,
    CalificacionDeleteView,
    CalificacionListView,
    CalificacionUpdateView,
    PromedioGeneralView,
)


urlpatterns = [
    path('', CalificacionListView.as_view(), name='listar'),
    path('crear/', CalificacionCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', CalificacionUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', CalificacionDeleteView.as_view(), name='eliminar'),
    path('promedio-general/', PromedioGeneralView.as_view(), name='promedio_general'),
]