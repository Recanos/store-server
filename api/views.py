from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductSerializer


class ProductModelViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "destroy"):
            self.permission_classes = [IsAdminUser]
        return super(ProductModelViewset, self).get_permissions()

class BasketModelViewset(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(BasketModelViewset, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        products = Product.objects.filter(id=product_id)
        if not products.exists():
            return Response({'product_id': 'no product with this id'}, status=status.HTTP_400_BAD_REQUEST)
        obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)