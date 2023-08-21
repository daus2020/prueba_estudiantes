from django.urls import path
from . import views
# from .views import indexView, listarView, registroView, loginView, logoutView, detalleView

urlpatterns = [
    path('', views.indexView, name='index'),
    path('listar/', views.listarView, name='listar'),
    path('registro/', views.registroView, name='registro'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('detalle/<str:pk>/', views.detalleView, name='detalle'),
]
