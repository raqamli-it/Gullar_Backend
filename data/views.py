from rest_framework import generics
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Flowers, Category, FlowersType, CategoryType, News, Favorite

from .serializers import FlowersSerializer, CategorySerializer, CategoryTypeListSerializer, FlowersTypeListSerializer, \
    FlowersTypeDetailSerializer, MarketListSerializer, MarketDetailSerializer, FlowerDetailSerializer, \
    CategoryDetailSerializer, CategoryTypeDetailSerializer, NewsSerializer, FavoriteSerializer
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


# Favorite

class FavoriteViewSet(APIView):
    def get(self, request):
        # Anonim foydalanuvchi ID'sini olish
        anonymous_user_id = request.COOKIES.get('anonymous_user_id')
        if not anonymous_user_id:
            return JsonResponse({'error': 'Anonymous user ID not found.'}, status=404)

        favorites = list(Favorite.objects.filter(anonymous_user_id=anonymous_user_id).values())
        return JsonResponse(favorites, safe=False)

    @csrf_exempt
    def post(self, request):
        data = request.data
        flower_id = data.get('flower')

        if not flower_id:
            return JsonResponse({'error': 'Flower ID not provided.'}, status=400)

        if request.user.is_authenticated:
            Favorite.objects.create(flower_id=flower_id, user=request.user)
        else:
            anonymous_user_id = request.COOKIES.get('anonymous_user_id')
            if not anonymous_user_id:
                return JsonResponse({'error': 'Anonymous user ID not found.'}, status=404)

            Favorite.objects.create(flower_id=flower_id, anonymous_user_id=anonymous_user_id)
        return JsonResponse({'favorite': 'create success'}, status=201)
