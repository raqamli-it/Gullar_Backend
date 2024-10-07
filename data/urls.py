from django.urls import path
from .views import CategoryDetail, FlowersTypeDetail, CategoryView, CategoryListView, \
    FlowersTypeListView, ReadyFlowers, MarketListView, MarketDetailView

urlpatterns = [
    path('ready-flowers/', ReadyFlowers.as_view()),
    path('categories/', CategoryView.as_view()),
    path('categories/list', CategoryListView.as_view()),
    path('category/detail/<int:id>/', CategoryDetail.as_view()),
    path('flowers-type/list', FlowersTypeListView.as_view()),
    path('flowers-type/detail/<int:id>/', FlowersTypeDetail.as_view()),
    path('market/list', MarketListView.as_view()),
    path('market/detail/<int:id>/', MarketDetailView.as_view()),
]
