from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram_backend import constants

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_CHARFIELD,
                            verbose_name='название')
    color = ColorField(default='#FF0000', verbose_name='цвет тэга')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_INGREDIENT,
                            verbose_name='продукт')
    measurement_unit = models.CharField(
        max_length=constants.MAX_LENGTH_CHARFIELD,
        verbose_name='единица измерения'
    )

    class Meta:
        ordering = ["id"]
        verbose_name = 'вид ингредиента'
        verbose_name_plural = 'Виды ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient'
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='вид ингрeдиента')
    amount = models.IntegerField(
        validators=[MinValueValidator(constants.MIN_VALUE)],
        verbose_name='колличество',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id']

    def __str__(self):
        return (f'{self.ingredient.name} '
                f'({self.ingredient.measurement_unit}) - {self.amount}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name="автор",
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=constants.MAX_LENGTH_CHARFIELD,
                            verbose_name='название рецепта')
    tags = models.ManyToManyField(Tag, through='TagRecipe',
                                  verbose_name='теги')
    text = models.TextField(verbose_name='описание рецепта')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(constants.MIN_VALUE),
                    MaxValueValidator(constants.MAX_VALUE)],
        verbose_name='время приготовления'
    )
    image = models.ImageField(
        upload_to=constants.IMAGE_DIR,
        default=None,
        blank=True,
        verbose_name='картинка'
    )
    added_to_favorites = models.ManyToManyField(
        User, related_name='added_to_favorites',
    )
    shopping_cart = models.ManyToManyField(User, related_name='shopping_cart')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def in_favorites_count(self):
        return self.added_to_favorites.count()


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тэг')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='рецепт')

    class Meta:
        verbose_name = 'тэги рецепта'
        verbose_name_plural = 'Тэги рецептов'

    def __str__(self):
        return f'{self.tag} {self.recipe}'
