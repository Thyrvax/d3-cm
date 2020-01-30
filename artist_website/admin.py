# Register your models here.

from django.contrib import admin

from .models import *


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.photos.create(picture=afile)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Event)
admin.site.register(MusicAlbum)
admin.site.register(AudioFile)
admin.site.register(PressArticle)  # " why the fuck "
admin.site.register(Page)  # " why the fuck "
admin.site.register(Category)  # " why the fuck "
admin.site.register(Prestation)  # " why the fuck "
admin.site.register(PrestationCat)  # " why the fuck "
