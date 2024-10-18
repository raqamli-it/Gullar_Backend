import uuid
from django.utils.deprecation import MiddlewareMixin

class AnonymousUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Foydalanuvchi tizimga kirmagan bo'lsa
        if not request.user.is_authenticated:
            # Cookie'da anonymous_user_id bor-yo'qligini tekshiramiz
            anonymous_user_id = request.COOKIES.get('anonymous_user_id')
            # Agar anonymous_user_id bo'lmasa, yangi UUID yaratamiz
            if not anonymous_user_id:
                anonymous_user_id = str(uuid.uuid4())
                request.anonymous_user_id = anonymous_user_id
            else:
                # Agar anonymous_user_id mavjud bo'lsa, uni saqlab qo'yamiz
                request.anonymous_user_id = anonymous_user_id
        else:
            # Foydalanuvchi tizimga kirgan bo'lsa, anonymous_user_id ni to'ldiramiz
            request.anonymous_user_id = None

    def process_response(self, request, response):
        # Agar foydalanuvchi anonim bo'lsa, cookie o'rnatamiz
        if not request.user.is_authenticated and request.anonymous_user_id:
            response.set_cookie('anonymous_user_id', request.anonymous_user_id)
        return response
