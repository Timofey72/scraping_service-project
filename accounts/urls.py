from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.register_view, name='signup_user'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user')
]
