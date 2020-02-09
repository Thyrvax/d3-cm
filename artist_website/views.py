import json
import os

from artist_website.models import Event, PressArticle, Page, Prestation, Album, AudioFile, MusicAlbum
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.contrib import messages


# Create your views here.
def view_events(request):
    events = Event.objects.all()
    return render(request, "artist_website/events_list.html", {"event_list": events, "events_page": "active"})


def view_articles(request):
    articles = PressArticle.objects.all()
    return render(request, "artist_website/article_list.html", {"article_list": articles,"press_page": "active"},)


def view_prestation(request, slug):
    presta = get_object_or_404(Prestation, slug=slug)
    return render(request, "artist_website/prestation_detail.html", {"prestation": presta, "presta_page": "active"})


def view_biography(request):
    bio = Page.objects.filter(title="Biographie")
    bio = bio[0]
    return render(request, "artist_website/page_detail.html", {"page": bio, "bio_page": "active"})


def view_links(request):
    liens = Page.objects.filter(title="Liens")
    liens = liens[0]
    return render(request, "artist_website/page_detail.html", {"page": liens, "link_page": "active"})


def view_videos(request):
    videos = Page.objects.filter(title="Vidéos")
    videos = videos[0]
    return render(request, "artist_website/page_detail.html", {"page": videos, "link_page": "active"})


def view_galleries(request):
    albums = Album.objects.all()
    complete_albums = {}
    for album in albums:
        complete_albums[album] = album.photos.all()
    return render(request, "artist_website/gallery.html", {"complete_albums": complete_albums, "gallery_page": "active"})


def view_audio_gallery(request):
    tracks = AudioFile.objects.all()
    return render(request, "artist_website/audio_gallery.html", {"tracks": tracks, "media_page": "active"})


def view_json_audio_gallery(request):
    audio_files = AudioFile.objects.all()

    # prepared a dict to populate the gallery, then parse as json
    audio_dict = []
    for this_file in audio_files:
        audio_dict.append({
            'track': this_file.tracknumber,  # link to thumbnail image
            'name': this_file.songname,  # link to enlarged image
            'duration': this_file.length,
            'file': os.path.split(this_file.songfile.url)[1],
            'text': this_file.comment,  # Title for the label or button
        })

    units_serialized = json.dumps(audio_dict)
    return render(request, "artist_website/audio_gallery_json.html", {"js_item": units_serialized})


def view_discography(request):
    discography = MusicAlbum.objects.all()
    return render(request, "artist_website/discography.html", {"discography": discography, "media_page": "active"})


def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['contact@catherinemathey.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, 'Votre message a bien été envoyé, merci.')
            return redirect('artist_website:email')
    return render(request, "artist_website/email.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')