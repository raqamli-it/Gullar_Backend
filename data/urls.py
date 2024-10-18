from django.urls import path
from .views import CategoryDetail, FlowersTypeDetail, CategoryView, CategoryTypeListView, \
    FlowersTypeListView, ReadyFlowers, MarketListView, MarketDetailView, FlowerDetailView, CategoryTypeDetail, \
    NewsListView, FavoriteViewSet

urlpatterns = [
    path('ready-flowers/', ReadyFlowers.as_view()),
    path('news/', NewsListView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('category-type/list', CategoryTypeListView.as_view()),
    path('category-type/detail/<int:id>/', CategoryTypeDetail.as_view()),
    path('category/detail/<int:id>/', CategoryDetail.as_view()),
    path('flowers-type/list', FlowersTypeListView.as_view()),
    path('flowers-type/detail/<int:id>/', FlowersTypeDetail.as_view()),
    path('flower/detail/<int:id>', FlowerDetailView.as_view()),
    path('market/list', MarketListView.as_view()),
    path('market/detail/<int:id>/', MarketDetailView.as_view()),

    path('favorites/', FavoriteViewSet.as_view()),
    # path('favorites/<int:pk>/', FavoriteViewSet.as_view()),



]
