from rest_framework import generics
from rest_framework.response import Response
from .models import Flowers, Category, FlowersType, CategoryType, News
from .serializers import FlowersSerializer, CategorySerializer, CategoryTypeListSerializer, FlowersTypeListSerializer, \
    FlowersTypeDetailSerializer, MarketListSerializer, MarketDetailSerializer, FlowerDetailSerializer, \
    CategoryDetailSerializer, CategoryTypeDetailSerializer, NewsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadyFlowers(generics.ListAPIView):
    serializer_class = FlowersSerializer

    def get_queryset(self):
        return Flowers.objects.filter(ready=True)


# Flower

class FlowerDetailView(generics.RetrieveAPIView):
    queryset = Flowers.objects.all()
    serializer_class = FlowerDetailSerializer
    lookup_field = 'id'


# Category


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Faqat birinchi 4 kategoriyani olish
        return Category.objects.all().order_by('created_at')[:4]

    def get_serializer_context(self):
        # request obyektini kontekstga uzatamiz
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'id'


# Category Type

class CategoryTypeListView(generics.ListAPIView):
    queryset = CategoryType.objects.all()  # Barcha kategoriyalarni olish
    serializer_class = CategoryTypeListSerializer


class CategoryTypeDetail(generics.RetrieveAPIView):
    serializer_class = CategoryTypeDetailSerializer
    queryset = CategoryType.objects.all()
    lookup_field = 'id'


# Flowers Type

class FlowersTypeListView(generics.ListAPIView):
    queryset = FlowersType.objects.all()  # Barcha kategoriyalarni olish
    serializer_class = FlowersTypeListSerializer


class FlowersTypeDetail(generics.RetrieveAPIView):
    serializer_class = FlowersTypeDetailSerializer
    queryset = FlowersType.objects.all()
    lookup_field = 'id'


# Market

class MarketListView(generics.ListAPIView):
    serializer_class = MarketListSerializer

    def get_queryset(self):
        return User.objects.filter(role='market')


class MarketDetailView(generics.RetrieveAPIView):
    serializer_class = MarketDetailSerializer
    queryset = User.objects.filter(role='market')
    lookup_field = 'id'


# News

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()  # Barcha kategoriyalarni olish
    serializer_class = NewsSerializer


