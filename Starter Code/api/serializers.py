from .models import Product, Order, OrderItem, User
from rest_framework import serializers

class  ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= (
            "id",
            "name", 
            "price",
            "stock"
        )

    def validate_price(self, value):
        if value <=0 :
            raise serializers.ValidationError(
                "Price must be grater than 0"
            )
        return value
    
class OrderItemserializer(serializers.ModelSerializer):
    product_name= serializers.CharField(source= "product.name")
    product_price= serializers.DecimalField(
        source= "product.price",
        max_digits=10,
        decimal_places=2
        )

    class Meta:
        model= OrderItem
        fields= (
            "product_name",
            "product_price",
            "quantity",
            "order", 
            "item_subtotal"
            )


class orderserializer(serializers.ModelSerializer):
    items= OrderItemserializer(many=True, read_only=True)

    total_price= serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items= obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)        


    class Meta:
        model= Order
        fields = (
            "order_id", 
            "user",
            "created_at", 
            "status",
            "items", 
            "total_price"
            )
        

class ProductInfoSerializers(serializers.Serializer):
    products= Product.objects.all()
    max_price= serializers.DecimalField(max_digits=10, decimal_places=2)
    count= serializers.IntegerField()