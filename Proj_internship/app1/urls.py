from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('forget/<int:id>', views.forget),
    path('otp/<int:id>', views.Otp),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('Logout/<int:id>/', views.Logout),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
