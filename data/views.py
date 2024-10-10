from rest_framework import generics
from rest_framework.response import Response
from .models import Flowers, Category, FlowersType
from .serializers import FlowersSerializer, CategorySerializer, CategoryListSerializer, FlowersTypeListSerializer, \
    FlowersTypeDetailSerializer, MarketListSerializer, MarketDetailSerializer, FlowerDetailSerializer
from django.db.models import F, Case, When
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadyFlowers(generics.ListAPIView):
    serializer_class = FlowersSerializer

    def get_queryset(self):
        return Flowers.objects.filter(ready=True)


class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = FlowersTypeDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'id'


class FlowersTypeDetail(generics.RetrieveAPIView):
    serializer_class = FlowersTypeDetailSerializer
    queryset = FlowersType.objects.all()
    lookup_field = 'id'



class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Faqat birinchi 4 kategoriyani olish
        return Category.objects.all().order_by('created_at')[:4]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()  # Barcha kategoriyalarni olish
    serializer_class = CategoryListSerializer


class FlowersTypeListView(generics.ListAPIView):
    queryset = FlowersType.objects.all()  # Barcha kategoriyalarni olish
    serializer_class = FlowersTypeListSerializer


class MarketListView(generics.ListAPIView):
    serializer_class = MarketListSerializer

    def get_queryset(self):
        return User.objects.filter(role='market')


class MarketDetailView(generics.RetrieveAPIView):
    serializer_class = MarketDetailSerializer
    queryset =User.objects.filter(role='market')
    lookup_field = 'id'

    # def get_queryset(self):
    #     return User.objects.filter(role='market')

class FlowerDetailView(generics.RetrieveAPIView):
    queryset =Flowers.objects.all()
    serializer_class = FlowerDetailSerializer
    lookup_field = 'id'
