from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="movies/")
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, blank=True, related_name="movies")

    def __str__(self):
        return self.title