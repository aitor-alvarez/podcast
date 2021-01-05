from django.contrib import admin
from django.urls import path, include
from podcast.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_podcasts),
		path('podcast/<pk>', PodcastView.as_view()),
		path('search/', PodcastSearch.as_view()),
		path('search/auto/', autocomplete),
		path('authoring/', authoring_form),
		path('series/<series_id>', get_podcast_in_series),
		path('contributor/<contributor_id>', get_contributor_podcasts),
	  path('add_mailing/', add_to_mailinglist)

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
