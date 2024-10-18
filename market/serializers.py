from rest_framework import serializers
from django.contrib.auth import get_user_model

from data.models import Favorite

User = get_user_model()


class MarketRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'password_confirmation', 'full_name']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # Parol tasdiqlash maydonini o'chirish
        validated_data.pop('password_confirmation')

        market = User(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            role="market"
        )
        market.set_password(validated_data['password'])
        market.save()
        return market


class MarketLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")
        market = User.objects.filter(phone=phone).first()

        if market and market.check_password(password):
            request = self.context.get('request')
            self._update_anonymous_favorites(request, market)
            return market
        else:
            raise serializers.ValidationError("Invalid phone or password")

    def _update_anonymous_favorites(self, request, user):
        # Anonim foydalanuvchi ID'sini olish
        anonymous_user_id = request.COOKIES.get('anonymous_user_id')

        if anonymous_user_id:
            # anonymous_user_id bilan bog'liq barcha sevimlilarni topamiz
            favorites = Favorite.objects.filter(anonymous_user_id=anonymous_user_id)

            if favorites.exists():
                # bulk update: sevimlilarning barchasini bitta so'rovda yangilaymiz
                favorites.update(user=user, anonymous_user_id=None)
                # Cookie'dan anonymous_user_id ni o'chirib tashlaymiz
                request.COOKIES.pop('anonymous_user_id', None)  # Cookie o'chirish



# class MarketPasswordChangeSerializer(serializers.Serializer):
#     old_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_new_password = serializers.CharField(write_only=True)
#
#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError("Old password is incorrect.")
#         return value
#
#     def validate(self, data):
#         if data['new_password'] != data['confirm_new_password']:
#             raise serializers.ValidationError("New passwords do not match.")
#         return data
#
#     def save(self, **kwargs):
#         user = self.context['request'].user
#         user.set_password(self.validated_data['new_password'])
#         user.save()
#         return user
#
#
# class MarketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['avatar', 'description', 'full_name', 'job_category', 'job_id', 'role']
