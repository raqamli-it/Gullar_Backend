from rest_framework import serializers

from user.models import UserImage
from .models import Flowers, Category, FlowersType
from django.contrib.auth import get_user_model

User = get_user_model()


class FlowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowers
        fields = ['id', 'title', 'image', 'price_old', 'price_new']


class FlowersTypeDetailSerializer(serializers.ModelSerializer):
    flowers = FlowersSerializer(many=True, read_only=True, source='flowers_type')

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']


class CategoryDetailSerializer(serializers.ModelSerializer):
    flowers = FlowersSerializer(many=True, read_only=True, source='flowers_type')

    class Meta:
        model = FlowersType
        fields = ['id', 'title', 'flowers']


class CategorySerializer(serializers.ModelSerializer):
    flowers = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'flowers']

    def get_flowers(self, obj):
        flowers = obj.category.all().order_by('-created_at')[:4]
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
        fields = ['full_name', 'image']


class MarketDetailSerializer(serializers.ModelSerializer):
    flowers = FlowersSerializer(many=True, read_only=True, source='market')

    class Meta:
        model = User
        fields = ['full_name', 'desc', 'avatar', 'flowers']
