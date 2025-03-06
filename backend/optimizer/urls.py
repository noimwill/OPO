from django.urls import path
from . import views

urlpatterns = [
    path('optimize/', views.optimize_portfolio, name='optimize_portfolio'),
]