from rest_framework import serializers
from django.db.models import F
from django.db.models.functions import Coalesce

from user.models import UserImage
from .models import Flowers, Category, FlowersType
from django.contrib.auth import get_user_model

from .pagination import FlowersPagination

User = get_user_model()


class FlowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowers
        fields = ['id', 'title', 'image', 'price_old', 'price_new', 'discount', 'discount_percent']


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


class FlowersTypeDetailSerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        ready = self.context['request'].query_params.get('ready', None)
        discount = self.context['request'].query_params.get('discount', None)
        date = self.context['request'].query_params.get('date', None)
        premium = self.context['request'].query_params.get('premium', None)
        cheap = self.context['request'].query_params.get('cheap', None)
        flowers_queryset = obj.flowers.all()

        if ready is not None:
            # Filter qilish
            flowers_queryset = flowers_queryset.filter(ready=True)

        if discount is not None:
            flowers_queryset = flowers_queryset.filter(discount=True)

        if date is not None:
            flowers_queryset = flowers_queryset.order_by('-created_at')

        if premium is not None and cheap is None:
            # premium bo'yicha tartiblash
            flowers_queryset = flowers_queryset.annotate(
                price=Coalesce('price_new', F('price_old'))
            ).order_by('-price')

        elif cheap is not None and premium is None:
            # premium bo'yicha tartiblash
            flowers_queryset = flowers_queryset.annotate(
                price=Coalesce('price_new', F('price_old'))
            ).order_by('price')

        # Paginatsiyani qo'llash
        paginator = FlowersPagination()
        page = paginator.paginate_queryset(flowers_queryset, self.context['request'])
        if page is not None:
            return paginator.get_paginated_response(FlowersSerializer(page, many=True).data).data

        return FlowersSerializer(flowers_queryset, many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    flowers = FlowersSerializer(many=True, read_only=True, source='flowers')

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']


class CategorySerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        flowers = obj.flowers.all().order_by('-created_at')[:4]
        return FlowersSerializer(flowers, many=True).data


# listlar
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image']


class FlowersTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'image']


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
    flowers = FlowersSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'desc', 'avatar', 'flowers', 'is_open']
