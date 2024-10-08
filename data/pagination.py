from rest_framework.pagination import PageNumberPagination

class FlowersPagination(PageNumberPagination):
    page_size = 3  # Har bir sahifada 1 ta flower
    page_size_query_param = 'page_size'  # URL parametr sifatida sahifa hajmini o'zgartirish
    max_page_size = 10  # Maksimal sahifa hajmi