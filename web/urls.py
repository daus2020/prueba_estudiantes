from django.urls import path
from .views import indexView, listarView, registroView, loginView, logoutView

urlpatterns = [

    path('', indexView, name='index'),
    path('listar/', listarView, name='listar'),
    path('registro/', registroView, name='registro'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    # path('detalle/<int:pk>/', views.detalle, name = 'detalle'),
]
