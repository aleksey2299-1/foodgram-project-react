from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=16, default="#FF0000")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        ordering = ["id"]
        verbose_name = 'Вид ингредиента'
        verbose_name_plural = 'Виды ингредиентов'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return (f'{self.ingredient.name} '
                f'({self.ingredient.measurement_unit}) - {self.amount}')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name="author",
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to="recipes/images/",
                              null=True, default=None, blank=True)
    added_to_favorites = models.ManyToManyField(
        User, related_name='added_to_favorites',
    )
    shopping_cart = models.ManyToManyField(User, related_name='shopping_cart')

    def __str__(self):
        return self.name

    def in_favorites_count(self):
        return self.added_to_favorites.count()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
