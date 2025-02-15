from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from products.models import Product, Order


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'created', 'total_price', 'phone_number', 'is_paid']

#total_priceni olish
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

#mahsulot miqdorini tekshirish
    def validate_quantity(self, value):
        try:
            product_id = self.initial_data['product'] #initial_data dan mahsulot ID sini oladi.
            product = Product.objects.get(id=product_id)

            if value > product.stock:
                raise serializers.ValidationError("Bazada buncha mahsulot yo'q")

            if value < 1:
                raise serializers.ValidationError('1 dan katta miqdor kiriting')

            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product does not exist')

# yangi zakas yaratish
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        product = order.product
        product.stock -= order.quantity
        product.save()
        return order



