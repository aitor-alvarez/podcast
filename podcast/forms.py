from django import forms
from .models import Podcast, Language, Categories
from haystack.forms import SearchForm


class PodcastForm(forms.ModelForm):
	class Meta:
		model = Podcast
		exclude = ['created',]

	def __init__(self, *args, **kwargs):
		super(PodcastForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'



class PodcastSearchForm(SearchForm):
		language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False, empty_label='Select the language')
		content_area = forms.CharField(required=False, widget=forms.HiddenInput)

		def __init__(self, *args, **kwargs):
			super(PodcastSearchForm, self).__init__(*args, **kwargs)
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'


		def search(self):

			if self.cleaned_data['q'] =='' and self.cleaned_data['language']:
				sqs = self.searchqueryset.all()
			elif self.cleaned_data['q'] =='' and self.cleaned_data['content_area']:
				sqs = self.searchqueryset.all()
			else:
				sqs = super(PodcastSearchForm, self).search()
			if not self.is_valid():
				return self.no_query_found()

			if self.cleaned_data['language']:
				sqs = sqs.filter(language=self.cleaned_data['language'])

			if self.cleaned_data['content_area']:
				area = Categories.objects.filter(id=self.cleaned_data['content_area'])
				sqs = sqs.filter(content_area=area)

			return sqs


