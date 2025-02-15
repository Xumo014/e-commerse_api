import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from products.models import Order

from products.serializers import OrderSerializer


@receiver(post_save, sender=Order) #
def notify_admin(sender, instance, created, **kwargs):
    if created:  # Qachonki zakas yaratilsa bu func ishlaydi
        token = settings.TELEGRAM_BOT_TOKEN
        method = 'sendMessage'

        order_data = OrderSerializer(instance).data
        total_price = order_data['total_price']


        message_text = f"🛒 **Yangi buyurtma!**\n\n" \
                       f"🆔 Order ID: {instance.id}\n" \
                       f"📦 Mahsulot: {instance.product.name}\n" \
                       f"🔢 Miqdor: {instance.quantity}\n" \
                       f"💰 Umumiy narx: {total_price} UZS\n" \
                       f"👤 Mijoz: {instance.customer.username}\n" \
                       f"📞 Tel: {instance.phone_number}"
        response = requests.post(
                url=f'https://api.telegram.org/bot{token}/{method}',
                data={'chat_id': 5981915099, 'text': message_text}
        ).json()


