from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from foodgram_backend.constants import MAX_LENGTH_NAME
from users.managers import CustomUserManager
from users.validators import validate_username


class CustomBaseUser(AbstractBaseUser):
    username = models.CharField(max_length=MAX_LENGTH_NAME, unique=True,
                                validators=(validate_username,))
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=MAX_LENGTH_NAME,
                                  verbose_name='имя')
    last_name = models.CharField(max_length=MAX_LENGTH_NAME,
                                 verbose_name='фамилия')
    image = models.ImageField(blank=True, null=True,
                              verbose_name='картинка пользователя')
    is_staff = models.BooleanField(default=False)
    subscribe = models.ManyToManyField('CustomBaseUser')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        app_label = "users"
        db_table = "users"
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__exact='me'), name="name_not_me",
            ),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
