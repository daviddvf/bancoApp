from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.crear_cuenta, name='crear_cuenta'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('home/', views.pagina_principal, name='pagina_principal'),
    path('crear-cuenta/', views.crear_cuenta_bancaria, name='crear_cuenta_bancaria'),
    path('cuenta/<int:cuenta_id>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('cuenta/<int:cuenta_id>/depositar/', views.depositar_dinero, name='depositar_dinero'),
    path('cuenta/<int:cuenta_id>/transferir/', views.transferir_dinero, name='transferir_dinero'), 
    path('detalles_usuario/', views.detalles_usuario, name='detalles_usuario')

]
