from datetime import timedelta, datetime

from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, FlashSale, UserProductView



# Chegirma bo'ladigan mahsulotga

class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = '__all__'

    serializer_class = FlashSaleSerializer


#Product chegirmasini tekshirish
@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    #User mahsulotni avval ko'rganmi
    user_viewed = UserProductView.objects.filter(user=request.user, product=product).exists() #exists() faqat malumiot bor yo'qligini tekshiradi

    # Yaqin orada chegirma bormi
    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now()+timedelta(hours=24),
    ).first()

    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"Ushbu mahsulot {discount} % chegirmada",
            "start_time": start_time,
            "end_time": end_time
        })
    else:
        return Response({
            "message": "Ushbu mahsulotga  yaqin orada chegirma yo'q",
        })

