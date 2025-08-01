from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListApiView.as_view()),
    path("products/info", views.ProductInfoApiView.as_view()),
    path("products/<int:pk>", views.ProductDetailsApiView.as_view()),
    path("orders/", views.OrderListApiView.as_view()),
    path("orders/<int:pk>", views.OrderListApiView.as_view()),
    path("user-orders/", views.UserOrderListApiView.as_view(), name="user-orders"),
]
