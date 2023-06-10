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


class User(User):
    def get_short_name(self):
        return self.first_name


class FavouriteRecipes(models.Model):
    name = models.CharField(max_length=112)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Statistics(models.Model):
    recipes = models.IntegerField
    users = models.IntegerField


class MealBaseOptions(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Chat(models.Model):
    text = models.CharField(max_length=500)
    gpt = models.CharField(max_length=17000)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
