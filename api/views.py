from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from api import serializers
from api.models import ApiUser, Store, Item, Order
from api.serializers import UserSerializer, StoreSerializer, ItemSerializer, OrderSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


class StoreModelViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemModelViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        # Проверка типа пользователя
        user = self.request.user
        if user.user_type != 'supplier':
            raise PermissionDenied("Только поставщики могут добавлять товары.")
        serializer.save()

    def perform_update(self, serializer):
        # Проверка типа пользователя и доступного количества товара на складе
        user = self.request.user
        if user.user_type != 'supplier':
            raise PermissionDenied("Только поставщики могут изменять товары.")
        new_quantity = self.request.data.get('quantity')
        if new_quantity and new_quantity < 0:
            raise serializers.ValidationError("Количество товара не может быть отрицательным.")
        serializer.save()


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        # Проверка типа пользователя (должен быть потребитель)
        if request.user.user_type != 'consumer':
            return Response({'error': 'Только потребители могут забирать товары со склада.'},
                            status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object()
        new_quantity = request.data.get('quantity')

        # Проверка, что указанное количество товара доступно на складе
        if new_quantity is not None and 0 < new_quantity <= instance.quantity:
            instance.quantity -= new_quantity
            instance.save()
            return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
        elif new_quantity is not None and new_quantity <= 0:
            return Response({'error': 'Количество товара должно быть больше 0.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Недостаточно товара на складе.'},
                            status=status.HTTP_400_BAD_REQUEST)
