"""
URL configuration for StyleHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from HubApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'login'),
    path('register',views.register),
    path('customers',views.customers),
    path('login',views.login),  
    path('profile',views.profile),
    path('addp',views.openaddproduct),
    path('addproduct',views.addproduct),
    path('product',views.product_list),
    path('logout_button',views.logout),
    path('dashboard',views.dashhh),
    path('logoutout',views.loglog),
    path('viewproductt',views.viewproduct),
    path('productbuy/<int:id>/',views.openbuy),
    path('buyproduct/<int:id>',views.buy), 
    path('addtocart/<int:id>',views.addtocart),
    path('orders',views.order),
    path('cartt',views.cart_view, name='cartt'),
    path('order_view/',views.oder_view, name='order_view'),
    path('home',views.indexload),
    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:id>/', views.remove_cart, name='remove_cart'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),  
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),  


   path('forgot/', views.forgot_password, name='forgot_password'),

   path('viewcate/<str:category>',views.cate_all,name='viewcate'),

    
    
    
    
    
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    
    
    
    path('viewproduct/', views.viewproduct, name='viewproduct'),
    path('editproduct/<int:id>/', views.editproduct, name='editproduct'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),



    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   





