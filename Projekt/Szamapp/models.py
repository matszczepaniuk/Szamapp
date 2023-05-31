from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=64)


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    instructions = models.CharField(max_length=1024)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")


class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class FavouriteRecipes(models.Model):
    name = models.CharField(max_length=112)


class User(User):
    def get_short_name(self):
        return self.first_name


class Statistics(models.Model):
    recipes = models.IntegerField
    users = models.IntegerField
