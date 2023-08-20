from django.urls import path
from .views import indexView, listarView, registroView, loginView, logoutView, detalleView

urlpatterns = [

    path('', indexView, name='index'),
    path('listar/', listarView, name='listar'),
    path('registro/', registroView, name='registro'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('detalle/<str:pk>/', detalleView, name='detalle'),
]
