from django.urls import path
from . import views

urlpatterns = [
    path('rule/<id>/', views.rule, name = 'rule'),
    path('rule/', views.rule, name = 'rule')
]