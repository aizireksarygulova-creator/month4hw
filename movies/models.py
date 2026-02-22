from django.db import models

from users.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="movies/")
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, blank=True, related_name="movies")

    def __str__(self):
        return self.title