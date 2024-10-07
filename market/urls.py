from django.urls import path
from .views import MarketRegistrationView, MarketLoginView

urlpatterns = [
    path('register/', MarketRegistrationView.as_view(), name='worker-register'),
    path('login/', MarketLoginView.as_view(), name='worker-login'),
    # path('password-change/', WorkerPasswordChangeView.as_view(), name='worker-password-change'),
    #
    # path('worker/<int:id>/', WorkerDetailView.as_view(), name='worker-detail'),
    #
    # path('websocket/', websocket_test, name='websocket_test'),
]
