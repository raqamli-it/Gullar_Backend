from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'


class FlowersType(models.Model):
    image = models.ImageField(upload_to='flowers_type/', null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Flowers Type'
        verbose_name_plural = 'Flowers Types'


class Flowers(models.Model):
    market = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='market')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='category')
    flowers_type = models.ForeignKey(FlowersType, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='flowers_type')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='flowers/')
    price_old = models.DecimalField(max_digits=10, decimal_places=2)
    price_new = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_time = models.CharField(max_length=50, null=True, blank=True)
    delivery_price = models.CharField(max_length=50, null=True, blank=True)
    product_composition = models.CharField(max_length=150, null=True, blank=True)
    discount = models.BooleanField(default=False)
    discount_percent = models.IntegerField(null=True, blank=True)
    desc = models.TextField(default="", blank=True, null=True)
    ready = models.BooleanField(default=False)
    height = models.IntegerField()
    width = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Flower'
        verbose_name_plural = 'Flowers'
