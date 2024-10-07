from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MarketRegistrationSerializer, MarketLoginSerializer
    # WorkerPasswordChangeSerializer, WorkerSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


def websocket_test(request):
    return render(request, 'web.html')


class MarketRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = MarketRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        market = serializer.save()

        refresh = RefreshToken.for_user(market)

        return Response({
            'user': serializer.data,
            # "refresh": str(refresh),
            # "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class MarketLoginView(generics.GenericAPIView):
    serializer_class = MarketLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        market = serializer.validated_data

        refresh = RefreshToken.for_user(market)

        return Response({
            "access": str(refresh.access_token),
            "market": MarketRegistrationSerializer(market).data,
        }, status=status.HTTP_200_OK)

#
# class WorkerPasswordChangeView(generics.GenericAPIView):
#     serializer_class = MarketPasswordChangeSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response({"message": "Password updated successfully."})
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#
# class WorkerDetailView(generics.RetrieveAPIView):
#     serializer_class = WorkerSerializer
#
#     def get_queryset(self):
#         # Faqat 'role=worker' bo'lgan foydalanuvchilarni filtrlash
#         return User.objects.filter(role='worker')
#
#     def get(self, request, *args, **kwargs):
#         worker_id = kwargs.get('id')
#         # Filtrlashdan so'ng foydalanuvchini olish
#         worker = get_object_or_404(self.get_queryset(), id=worker_id)
#         serializer = self.get_serializer(worker)
#         return Response(serializer.data)