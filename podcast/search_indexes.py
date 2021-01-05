import datetime
from haystack import indexes
from .models import Podcast


class PodcastIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	description = indexes.CharField(model_attr='description')
	title = indexes.EdgeNgramField(model_attr='title')
	tags = indexes.EdgeNgramField(model_attr='tags')
	language = indexes.CharField(model_attr='language')
	content_area = indexes.CharField(model_attr='content_area')
	content_type = indexes.CharField(model_attr='content_type')


	def get_model(self):
		return Podcast

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(created__lte= datetime.datetime.now())

	def prepare_tags(self, object):
		return [tag.name for tag in object.tags.all()]
