from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('chart', views.chart, name='chart'),
    path('<str:name>', views.stock, name='stock')
]