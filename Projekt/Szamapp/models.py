from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=64)


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    instructions = models.CharField(max_length=8192)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")


class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class User(User):
    def get_short_name(self):
        return self.first_name


class FavouriteRecipes(models.Model):
    name = models.CharField(max_length=112)
    user = models.CharField(max_length=100, default=0)


class Statistics(models.Model):
    recipes = models.CharField(max_length=100, default=0)
    users = models.CharField(max_length=100, default=0)
