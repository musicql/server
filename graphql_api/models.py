from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=250)
    img_url = models.TextField()

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)
    pub_date = models.DateField()
    img_url = models.TextField()

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, related_name="songs", on_delete=models.CASCADE)
    pub_date = models.DateField()
    album = models.ForeignKey(Album, related_name="songs", on_delete=models.CASCADE)
    song_url = models.TextField()
    img_url = models.TextField()

    def __str__(self):
        return self.name
