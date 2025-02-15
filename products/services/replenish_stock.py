from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from products.models import Product
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes


@api_view(['POST'])
@swagger_auto_schema(operation_description="Admin replenishes stock for a product")
@permission_classes([IsAdminUser])

def admin_replanish_stock(request, product_id, amount):
    try:
        product = Product.objects.get(pk=product_id)
        # product.stock += int(amount)
        product.increase_stock(amount)
        product.save()

        return JsonResponse({'status': 'success', 'message': f'Successfully replenished stock by {amount}'})

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product does not exist'}, status=400)

    except ValueError:
        return HttpResponseBadRequest('Invalid input!')