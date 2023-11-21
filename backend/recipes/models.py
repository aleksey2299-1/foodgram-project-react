from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    # color = ColorField(default="#FF0000")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    measurement = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, verbose_name="recipes",
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    tag = models.ManyToManyField(Tag, through='TagRecipe')
    desc = models.TextField()
    time = models.CharField(max_length=10)
    image = models.ImageField(upload_to="recipes/images/",
                              null=True, default=None, blank=True)
    ingridients = models.ManyToManyField(Ingridient,
                                         through='IngridientRecipe')

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngridientRecipe(models.Model):
    ingridient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingridient} {self.recipe}'
