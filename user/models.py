from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import pytz

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')

        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, full_name, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('manager', 'manager'),
        ('client', 'client'),
        ('market', 'market'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(blank=True, null=True)
    desc = models.TextField(max_length=3000)



    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    open_time = models.TimeField(null=True, blank=True)  # Ochilish vaqti
    close_time = models.TimeField(null=True, blank=True)  # Yopilish vaqti



    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    @property
    def is_open(self):
        """
        Market ochiq yoki yopiq ekanligini soat va minut bo'yicha tekshiradi
        """
        # O'zbekiston vaqt zonasini olish
        uzbekistan_tz = pytz.timezone('Asia/Tashkent')
        current_time = timezone.now().astimezone(uzbekistan_tz).time()

        # Agar rol 'market' bo'lsa va open_time yoki close_time None bo'lsa, True qaytar
        if self.role == 'market':
            if self.open_time is None or self.close_time is None:
                return True

            # Faqat soat va minut bo'yicha tekshirish
            if self.open_time <= current_time <= self.close_time:
                return True

        return False

    def __str__(self):
        return f"{self.full_name} | {self.phone}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['created_at']


class UserImage(models.Model):
    user = models.ForeignKey('AbstractUser', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = 'User Image'
        verbose_name_plural = 'User Images'
