"""
URL configuration for ProiectREST project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from hr import views
from rest_framework import routers
from django.contrib.auth import views as auth
from hr.views import profile
from hr.views import laptopuri_view
from hr.views import telefoane_view
from hr.views import search_view
from hr.views import product_list_view
from hr.views import wishlist_view
from hr.views import add_to_cart
from hr.views import cart_view
from hr.views import checkout
from hr.views import purchase
from hr.views import history


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.index, name="index"),
    path('login/', views.login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
    path('profile/', profile, name='profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile_or_user_profile/', views.profile_or_user_profile, name='profile_or_user_profile'),
    path('laptopuri/', laptopuri_view, name='laptopuri'),
    path('telefoane/', telefoane_view, name='telefoane'),
    path('search/', search_view, name='search_results'),
    path('product_list/', product_list_view, name='product_list'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout, name='checkout'),
    path('purchase/', purchase, name='purchase'),
    path('history/', history, name='history'),
    path('searchresults/', views.search, name='searchresults'),
]
