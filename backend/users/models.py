from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from users.validators import username_validator


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, first_name, last_name, password):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name,
                         last_name, password):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomBaseUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True,
                                validators=[username_validator])
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    image = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    subscribe = models.ManyToManyField('CustomBaseUser')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        app_label = "users"
        db_table = "users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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
