from rest_framework import serializers
from django.contrib.auth import get_user_model

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
            return market
        else:
            raise serializers.ValidationError("Invalid phone or password")








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
