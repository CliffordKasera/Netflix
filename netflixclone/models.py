from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=20)
    email = models.EmailField
    def __str__(self):
            return self.username

class User_Fav(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.IntegerField()
    def __str__(self):
        return (self.user_id, self.movie)
