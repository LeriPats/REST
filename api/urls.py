from rest_framework.routers import DefaultRouter
from django.urls import path
from api.views import UserModelViewSet, StoreModelViewSet, ItemModelViewSet, OrderModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('stores', StoreModelViewSet)
router.register('items', ItemModelViewSet)
router.register('orders', OrderModelViewSet)


urlpatterns = [
    path('warehouses/create/',
         StoreModelViewSet.as_view({'get': 'list'}),
         name='create-warehouse'),
    path('products/<int:pk>/withdraw/',
         OrderModelViewSet.as_view(({'get': 'list'})),
         name='withdraw-product'),
    ]

urlpatterns.extend(router.urls)
