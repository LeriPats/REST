from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
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

    def perform_create(self, serializer):
        # Проверка типа пользователя
        user = self.request.user
        if user.user_type != 'consumer':
            raise PermissionDenied("Только покупатели могут делать заказы.")
        serializer.save()

    def perform_update(self, serializer):
        # Проверка типа пользователя и доступного количества товара на складе
        user = self.request.user
        if user.user_type != 'consumer':
            raise PermissionDenied("Только покупатели могут изменять заказы.")
        new_quantity = self.request.data.get('quantity')
        if new_quantity and new_quantity < 0:
            raise serializers.ValidationError("Количество товара не может быть отрицательным.")
        serializer.save()