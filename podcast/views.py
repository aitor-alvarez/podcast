from django.shortcuts import render
from podcast.models import *
from django.views.generic import DetailView
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from .forms import PodcastForm, PodcastSearchForm
from haystack.generic_views import SearchView
from collections import Counter
from utils.mailchimp import get_config
from mailchimp_marketing.api_client import ApiClientError


def get_podcast_in_series(request, series_id):
	podcasts = Podcast.objects.filter(series=series_id)
	series = Series.objects.get(id=series_id)
	return render(request, template_name='podcast/series.html', context={'series': series, 'podcasts':podcasts})


def get_contributor_podcasts(request, contributor_id):
	contributor = Contributor.objects.get(id=contributor_id)
	podcasts = Podcast.objects.filter(contributor=contributor_id).order_by('-id')[:5]
	return render(request, template_name='podcast/contributor.html', context={'contributor': contributor, 'podcasts': podcasts})


def get_podcasts(request):
	podcasts = Podcast.objects.all().order_by('-id')
	podcasts_last =podcasts[:5]
	languages = podcasts.values('id').distinct()
	languages = Language.objects.filter(id__in=languages)
	contributors = podcasts.values('id').distinct()
	contributors = Contributor.objects.filter(id__in=contributors)
	return render(request, template_name='podcast/home.html', context={'podcasts': podcasts_last, 'languages': languages,
	                                                                   'contributors': contributors})


class PodcastView(DetailView):
	model = Podcast

	def get_context_data(self, *args, **kwargs):
		context = super(PodcastView, self).get_context_data(*args, **kwargs)
		print(self.object.tags)
		tags =[tag.id for tag in self.object.tags.all()]
		related = Podcast.objects.filter(tags__in=tags).distinct().exclude(id=self.object.id)
		context['related'] = related
		return context


class PodcastSearch(SearchView):
	form_class = PodcastSearchForm
	template = 'search/search.html'
	paginate_by = 5
	context_object_name = 'object_list'



	def get_context_data(self, *args, **kwargs):
		context = super(PodcastSearch, self).get_context_data(*args, **kwargs)
		categories = [(s.object.content_area, s.object.content_area.id)  for s in context['object_list']]
		categories = Counter(categories)
		categories = [(c, categories[c]) for c in categories]
		context.update({'categories': categories})

		languages = [(s.object.language, s.object.language.id) for s in context['object_list']]
		languages = Counter(languages)
		languages= [(c, languages[c]) for c in languages]
		context.update({'languages': languages})

		content_type = [(s.object.get_content_type_display(), s.object.content_type) for s in context['object_list']]
		content_type = Counter(content_type)
		content_type = [(c, content_type[c]) for c in content_type]
		context.update({'content_type': content_type})

		return context



def autocomplete(request):
	sug1=[]
	sqs1 = SearchQuerySet().models(Podcast).autocomplete(title=request.GET.get('q', ''))[:5]
	sqs2 = SearchQuerySet().models(Podcast).autocomplete(tags=request.GET.get('q', ''))[:5]
	for result in sqs2:
		for tag in result.tags.split(','):
			sug1.append(tag)
	sug2 = [result.title for result in sqs1]
	suggestions = sug1+sug2
	the_data = json.dumps({'results': suggestions})
	return HttpResponse(the_data, content_type='application/json')


@login_required
def authoring_form(request):
	podform = PodcastForm()
	if request.method =='POST':
		if podform.is_valid(request.POST):
			podform.save()
	else:
		podform = PodcastForm()
	return render(request, template_name='podcast/authoring.html', context={'form': podform})


def add_to_mailinglist(request):
	if request.is_ajax() and request.method == "POST":
		email = request.POST['data']
		client, list_id = get_config()
		try:
			response = client.lists.add_list_member(list_id, {"email_address": email, "status": "Subscribed"})
			return HttpResponse('You have been added to our mailing list!')
		except ApiClientError as error:
			return HttpResponse('This email is already in our mailing list.')


