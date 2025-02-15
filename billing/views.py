from django.shortcuts import render

from ecommerse import settings
from .models import Payment
from rest_framework.response import Response
from rest_framework import views, status
import stripe
from .serializers import PaymentSerializer
from products.models import Order

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateChargeView(views.APIView):


    def post(self, request, *args, **kwargs):
        stripe_token = request.data.get('stripe_token')
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_amount = order.product.price * order.quantity
            uzs = 13020
            total_amount_uzs = total_amount / uzs
            charge = stripe.Charge.create(
                amount=int(total_amount_uzs*100),
                currency='usd',
                source=stripe_token
            )

            Payment.objects.create(
                order=order,
                stripe_charge_id=charge["id"],
                amount=total_amount

            )
            if order.is_paid:
                return Response({"status": "Is_paid=True"})
            else:

                order.is_paid = True
                order.save()


                return Response({'status':"Payment successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
