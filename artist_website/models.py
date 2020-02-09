from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.utils.text import slugify
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import mutagen

# Parent class for event and pressArticle
class Item(models.Model):
    title = models.CharField(verbose_name="Titre", max_length=250)
    text = RichTextField(verbose_name="Description", null=False)
    isPublished = models.BooleanField(verbose_name='Visible', default=False)
    publicationDate = models.DateTimeField(verbose_name="Date de publication", blank=True, null=True)
    creationDate = models.DateTimeField(verbose_name="Date de création", editable=False, blank=True)
    modificationDate = models.DateTimeField(verbose_name="Dernière modification", editable=False, null=True)
    slug = models.SlugField(verbose_name="url", unique=True, max_length=50, blank=True)

    class Meta:
        verbose_name = "Publications"
        ordering = ['-creationDate']

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèlesd
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        if self.isPublished:
            if not self.publicationDate:
                self.publicationDate = timezone.localtime()


        # set creation date if empty, else update modification date
        if not self.creationDate:
            self.creationDate = timezone.localtime()
        else:
            self.modificationDate = timezone.localtime()

        super(Item, self).save(*args, **kwargs)


class Event(Item):
    location = models.CharField(verbose_name="Où", max_length=250, null=True, blank=True)
    eventDate = models.CharField(verbose_name="Quand", max_length=250, null=True, blank=True)
    picture = models.ImageField(upload_to='event_picture', null=True, blank=True)
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFit(height=150)],
                                       format='JPEG',
                                       options={'quality': 60})

    class Meta:
        verbose_name = "Évènement"
        ordering = ['-publicationDate']


class PressArticle(Item):
    date = models.CharField(verbose_name="Date de parution", max_length=250, null=True, blank=True)
    source = models.CharField(verbose_name="Source", max_length=500, null=True, blank=True)
    picture = models.ImageField(upload_to='article_picture', null=True, blank=True)
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFit(height=150)],
                                       format='JPEG',
                                       options={'quality': 60})

    class Meta:
        verbose_name = "Article de presse"
        verbose_name_plural = "Articles de presse"
        ordering = ['-publicationDate']


class Category(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=50)

    class Meta:
        verbose_name = "Catégorie"
        ordering = ['name']

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.name


class Page(Item):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Page"
        ordering = ['-creationDate']


class PrestationCat(models.Model):
    name = models.CharField(verbose_name="Nom de la catégorie", max_length=50)

    class Meta:
        verbose_name = "Catégorie Prestation"
        ordering = ['name']

    def __str__(self):
        return self.name


class Prestation(Item):
    category = models.ForeignKey(PrestationCat, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Prestation"
        ordering = ['-creationDate']

    def __str__(self):
        return self.title


class Album(models.Model):
    titre = models.CharField(verbose_name="Nom de l'album", max_length=50)
    publicationDate = models.DateTimeField(verbose_name="Date de publication", blank=True, null=True)

    class Meta:
        verbose_name = "Album photo"
        ordering = ['-publicationDate']

    def __str__(self):
        return self.titre


class Photo(models.Model):
    album = models.ForeignKey(Album,  related_name="photos", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='gallery')
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFit(200, 200)],
                                       format='JPEG',
                                       options={'quality': 60})

    def __str__(self):
        return self.picture.url


class AudioFile(models.Model):
    tracknumber = models.IntegerField(verbose_name='Ordre', unique=True, null=True, blank=True)
    songname = models.CharField(verbose_name='Titre', max_length=150)
    songfile = models.FileField(verbose_name='Fichier', upload_to='audio')
    comment = RichTextField(verbose_name='Commentaire', null=True, blank=True,)
    length = models.CharField(verbose_name='Durée',  max_length=6, null=True, blank=True)

    def __str__(self):
        return self.songname

    def save(self, *args, **kwargs):
        audio_info = mutagen.File(self.songfile).info
        song_length = int(audio_info.length)
        minutes = str(song_length // 60)
        seconds = str(song_length % 60)
        if len(seconds) == 1:
            self.length = str(song_length // 60) + ':0' + str(song_length % 60)
        else:
            self.length = str(song_length // 60) + ':' + str(song_length % 60)
        super(AudioFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Fichiers audio"
        ordering = ['tracknumber']


class MusicAlbum(Item):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Album"
        ordering = ['title']
