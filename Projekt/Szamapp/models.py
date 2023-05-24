from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    instructions = models.CharField(max_length=1024)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    favourites = models.ForeignKey(FavouriteRecipes, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=64)


class FavouriteRecipes(models.Model):
    name = models.CharField(max_length=112)


class Statistics(models.Model):
    recipes = models.IntegerField
    users = models.IntegerField
