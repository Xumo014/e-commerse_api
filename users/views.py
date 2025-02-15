# Create your views here.
import vonage
from django.contrib.auth import get_user_model
import requests
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SMSSerializer, VerifyCodeSerializer
from rest_framework import viewsets, status
User = get_user_model()
import random
from ecommerse import settings


class SMSLoginViewSet(viewsets.ViewSet):

    def send_sms(self, request):
        serializer = SMSSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            verification_code = str(random.randint(10000, 99999))

            client = vonage.VonageClient(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
            sms = vonage.Sms(client)

            response = sms.send_message({
                "from": settings.VONAGE_BRAND_NAME,  # Sender ID
                "to": phone_number,
                "text": f"Sizning tasdiqlash kodingiz: {verification_code}",
            })



            if response.status_code == 200:
                cache.set(phone_number, verification_code, 120)

                return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)


            return Response({'message': "Failed to sent sms"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def verify_sms(self, request):
        serializer = VerifyCodeSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cashed_code = cache.get(phone_number)

            if verification_code == cashed_code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                if created:
                    user.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),

                })

            return Response({'message': "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)