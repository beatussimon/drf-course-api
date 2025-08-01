from django.shortcuts import render
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, orderserializer, OrderItemserializer, ProductInfoSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ProductListApiView(generics.ListAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer


class ProductDetailsApiView(generics.RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

class UserProductListApiView(generics.RetrieveAPIView):
    queryset= Product.objects.all()
    

class OrderListApiView(generics.ListAPIView):
    queryset= Order.objects.prefetch_related("items", "items__product").all()
    serializer_class= orderserializer

class UserOrderListApiView(generics.ListAPIView):
    queryset= Order.objects.prefetch_related("items", "items__product").all()
    serializer_class= orderserializer
    permission_classes= [IsAuthenticated
                         ]

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(user=self.request.user)

class OrderDetailsApiView(generics.RetrieveAPIView):
    queryset= Order.objects.all()

class ProductInfoApiView(APIView):
    def get(request):
        products= Product.objects.all()
        serializer= ProductInfoSerializers({
            "products": products,
            "count":len(products),
            "max_price":products.aggregate(alias= Max("price"))["alias"]
        })
        return Response(serializer.data)  