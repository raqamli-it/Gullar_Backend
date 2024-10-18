from rest_framework import serializers
from django.db.models import F
from django.db.models.functions import Coalesce

from user.models import UserImage
from .models import Flowers, Category, FlowersType, CategoryType, News, Favorite
from django.contrib.auth import get_user_model

from .pagination import FlowersPagination

User = get_user_model()


def get_flowers_for_object(obj, context):
    request = context['request']
    ready = request.query_params.get('ready', None)
    discount = request.query_params.get('discount', None)
    date = request.query_params.get('date', None)
    premium = request.query_params.get('premium', None)
    cheap = request.query_params.get('cheap', None)
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)

    flowers_queryset = obj.flowers.all()

    if ready is not None:
        flowers_queryset = flowers_queryset.filter(ready=True)

    if discount is not None:
        flowers_queryset = flowers_queryset.filter(discount=True)

    if date is not None:
        flowers_queryset = flowers_queryset.order_by('-created_at')

    if min_price is not None or max_price is not None:
        # price_new yoki price_old bilan narxni qo'shish va filtr qilish
        flowers_queryset = flowers_queryset.annotate(
            price=Coalesce('price_new', F('price_old'))
        )

        # min_price va max_price ni qo'llash
        if min_price is not None:
            flowers_queryset = flowers_queryset.filter(price__gte=min_price)

        if max_price is not None:
            flowers_queryset = flowers_queryset.filter(price__lte=max_price)

    if premium is not None and cheap is None:
        flowers_queryset = flowers_queryset.annotate(
            price=Coalesce('price_new', F('price_old'))
        ).order_by('-price')

    elif cheap is not None and premium is None:
        flowers_queryset = flowers_queryset.annotate(
            price=Coalesce('price_new', F('price_old'))
        ).order_by('price')

    # Paginatsiyani qo'llash
    paginator = FlowersPagination()
    page = paginator.paginate_queryset(flowers_queryset, request)
    if page is not None:
        return paginator.get_paginated_response(FlowersSerializer(page, many=True, context=context).data).data

    return FlowersSerializer(flowers_queryset, many=True, context=context).data


# Flower

class FlowersSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Flowers
        fields = ['id', 'title', 'image', 'price_old', 'price_new', 'discount', 'discount_percent']

    def get_image(self, obj):
        request = self.context.get('request')  # request obyektini olamiz
        if obj.image:
            return request.build_absolute_uri(obj.image.url)  # to'liq URL yaratamiz
        return None


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar']


class FlowerDetailSerializer(serializers.ModelSerializer):
    market = MarketSerializer()

    class Meta:
        model = Flowers
        fields = ['id', 'image', 'title', 'price_old', 'price_new', 'discount', 'discount_percent', 'delivery_time',
                  'delivery_price', 'product_composition', 'desc', 'height', 'width', 'market']


class CategorySerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        flowers = obj.flowers.all().order_by('-created_at')[:4]
        return FlowersSerializer(flowers, many=True, context=self.context).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        return get_flowers_for_object(obj, self.context)


# Category Type


class CategoryTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = ['id', 'title', 'image']


class CategoryTypeDetailSerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        return get_flowers_for_object(obj, self.context)


# Flowers Type

class FlowersTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'image']


class FlowersTypeDetailSerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        return get_flowers_for_object(obj, self.context)


# Market


class MarketImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']


class MarketListSerializer(serializers.ModelSerializer):
    image = MarketImageSerializer(many=True, read_only=True, source='images')

    class Meta:
        model = User
        fields = ['id', 'full_name', 'image', 'is_open']


class MarketDetailSerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'desc', 'avatar', 'flowers', 'is_open']

    def get_flowers(self, obj):
        return get_flowers_for_object(obj, self.context)



# News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'market']


# Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    flower = FlowersSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'flower', 'user', 'anonymous_user_id']