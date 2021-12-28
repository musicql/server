import graphene
from graphene_django import DjangoObjectType

from graphql_api import models


class Album(DjangoObjectType):
    class Meta:
        model = models.Album


class Artist(DjangoObjectType):
    class Meta:
        model = models.Artist


class Song(DjangoObjectType):
    class Meta:
        model = models.Song


class ArtistInput(graphene.InputObjectType):
    name = graphene.String()
    img_url = graphene.String()

class SongInput(graphene.InputObjectType):
    name = graphene.String()
    pub_date = graphene.Date()
    album_id = graphene.Int()
    song_url = graphene.String()
    img_url = graphene.String()


class AlbumInput(graphene.InputObjectType):
    name = graphene.String()
    artist_id = graphene.Int()
    pub_date = graphene.Date()
    img_url = graphene.String()


class CreateArtist(graphene.Mutation):
    class Arguments:
        input = ArtistInput(required=True)

    ok = graphene.Boolean()
    artist = graphene.Field(Artist)

    @staticmethod
    def mutate(root, info, input):
        instance = models.Artist(name=input.name)
        try:
            instance.save()
        except Exception:
            return CreateArtist(ok=False, artist=None)

        return CreateArtist(ok=True, artist=instance)


class CreateSong(graphene.Mutation):
    class Arguments:
        input = SongInput(required=True)

    ok = graphene.Boolean()
    song = graphene.Field(Song)

    @staticmethod
    def mutate(root, info, input):
        album = models.Album.objects.get(pk=input.album_id)
        if not models.Artist.objects.filter(pk=album.pk).exists():
            return CreateSong(ok=False, song=None)

        instance = models.Song(name=input.name, artist=album.artist, pub_date=input.pub_date, album=album, song_url=input.song_url, img_url=input.img_url)
        try:
            instance.save()
        except Exception:
            return CreateSong(ok=False, song=None)

        return CreateSong(ok=True, song=instance)


class CreateAlbum(graphene.Mutation):
    class Arguments:
        input = AlbumInput(required=True)

    ok = graphene.Boolean()
    album = graphene.Field(Album)

    @staticmethod
    def mutate(root, info, input):

        artist = models.Artist.objects.get(pk=input.artist_id)
        if not models.Artist.objects.filter(pk=artist.pk).exists():
            return CreateAlbum(ok=False, album=None)

        instance = models.Album(name=input.name, artist=artist, pub_date=input.pub_date, img_url=input.img_url)
        try:
            instance.save()
        except Exception:
            return CreateAlbum(ok=False, album=None)

        return CreateAlbum(ok=True, album=instance)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    artist = graphene.Field(Artist, id=graphene.Int())
    album = graphene.Field(Album, id=graphene.Int())
    song = graphene.Field(Song, id=graphene.Int())

    artists = graphene.List(Artist)
    albums = graphene.List(Album)
    songs = graphene.List(Song)

    def resolve_artist(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return models.Artist.objects.get(pk=id)

        return None

    def resolve_album(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return models.Album.objects.get(pk=id)

        return None

    def resolve_song(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return models.Song.objects.get(pk=id)

        return None

    def resolve_artists(self, info, **kwargs):
        return models.Artist.objects.all()

    def resolve_albums(self, info, **kwargs):
        return models.Album.objects.all()

    def resolve_songs(self, info, **kwargs):
        return models.Song.objects.all()


class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    create_album = CreateAlbum.Field()
    create_song = CreateSong.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
