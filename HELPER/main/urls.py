from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('register/', views.RegisterPageView.as_view(), name='register_page'),
    path('login/', views.LoginPageView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('crypto_manage/', views.CryptoPageView.as_view(), name='crypto_page'),
    path('share_manage/', views.SharePageView.as_view(), name='share_page'),
]