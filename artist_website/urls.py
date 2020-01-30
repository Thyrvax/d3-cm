from django.conf.urls import url
from django.urls import path


from artist_website import views

app_name="artist_website"

urlpatterns = [
    url(r"^$", views.view_articles, name="home"),
    path('presse/', views.view_articles, name="presse"),
    path('biographie/', views.view_biography, name="biographie"),
    # path('press/<int:id>', views.view_snippet, name="snippet"),
    path('evenements/', views.view_events, name='events'),
    path('discographie/', views.view_discography, name = 'discographie'),
    path('morceaux-en-ecoute/', views.view_audio_gallery, name = 'mp3'),
    path('prestation/<slug:slug>/', views.view_prestation, name='prestation'),
    path('liens/', views.view_links, name="links"),
    path('videos/', views.view_videos, name="videos"),
    path('galerie/', views.view_galleries, name="gallery"),
    path('email/', views.emailView, name="email"),
    path('success/', views.successView, name="success"),

    # path('new', views.view_new, name='new'),
]
