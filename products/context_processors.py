from products.models import Basket


def baskets(request):
    return {'baskets' : Basket.objects.filter(user=request.user) if request.user.is_authenticated else []}




