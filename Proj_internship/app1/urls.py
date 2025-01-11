from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.Login),
    path('forget/<int:id>', views.forget),
    path('otp/<int:id>', views.Otp),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
]
