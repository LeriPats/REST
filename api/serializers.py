from rest_framework import serializers
from rest_framework import validators

from api.models import ApiUser, Store, Item, Order


class UserSerializer(serializers.Serializer):
    class Meta:
        model = ApiUser
        fields = ('id', 'username', 'email', 'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    user_type = serializers.ChoiceField(choices=('consumer', 'supplier'))

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        user.user_type = validated_data.get('user_type', 'consumer')
        user.save()
        return user


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'quantity', 'store')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class ValidationError(Exception):
    pass
