from rest_framework.routers import DefaultRouter

from api.views import UserModelViewSet, StoreModelViewSet, ItemModelViewSet, OrderModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('stores', StoreModelViewSet)
router.register('items', ItemModelViewSet)
router.register('orders', OrderModelViewSet)


urlpatterns = [

]

urlpatterns.extend(router.urls)
