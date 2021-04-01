from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('shop/<str:id>/', views.shop, name="shop"),
    path('shop/<str:id>/<str:pid>', views.SingleProduct, name="singel_product"),
    path('login', views.customerLogin, name="customer_login"),
    path('logout', views.customerLogout, name="customer_logout"),
    path('register', views.customerRegister, name="customer_register"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('pharmacy/home', views.pharmacyHome, name="pharmacy_home"),
    path('pharmacy/register', views.pharmacyRegister, name='pharmacy_register'),
    path('pharmacy/login', views.pharmacyLogin, name='pharmacy_login'),
    path('pharmacy/logout', views.pharmacyLogout, name="pharmacy_logout"),
    path('pharmacy/addproduct', views.pharmacyAddProduct,
         name="pharmacy_addproduct"),

    path('pharmacy/dashboard', views.pharmacyDashboard, name="pharmacy_dashboard"),

    path('pharmacy/dashboard/update/<str:id>',
         views.pharmacyDashboardUpdateOrder, name="pharmacy_dashboard_update_order"),

    path('pharmacy/dashboard/items/<str:id>',
         views.pharmacyDashboardOrderItems, name="pharmacy_dashboard_order_items"),
    path('pharmacy/dashboard/address/<str:id>',
         views.pharmacyDashboardOrderAddress, name="pharmacy_dashboard_order_address"),
    path('pharmacy/delivereddashboard',
         views.pharmacyDeliveredDashboard, name="pharmacy_delivered_dashboard"),

]
