from django.db import models
import datetime

type_choices= (
	('V', 'Video'),
	('A', 'Audio')
)


class Language(models.Model):
	name = models.CharField(max_length=150)
	image = models.ImageField(blank=True)

	def __str__(self):
		return str(self.name)


class Contributor(models.Model):
	name = models.CharField(max_length=150)
	image = models.ImageField(blank=True)
	about_me = models.TextField(blank=False)
	website = models.URLField(blank=True)
	contact = models.CharField(max_length=150)

	def __str__(self):
		return str(self.name)


class Categories(models.Model):
	name = models.CharField(max_length=150)

	def __str__(self):
		return str(self.name)


class Series(models.Model):
	name = models.CharField(max_length=150)

	def __str__(self):
		return str(self.name)

class Document(models.Model):
	document = models.URLField()


class Material(models.Model):
	title = models.CharField(max_length=255, blank=True)
	text = models.TextField(blank=True)
	documents = models.ManyToManyField(Document)

	def __str__(self):
		return str(self.title)



class Tags(models.Model):
	name = models.CharField(max_length=150)
	visible = models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)


class Podcast(models.Model):
	title = models.CharField(max_length=250, blank=False)
	description = models.TextField(blank=False)
	blurb = models.TextField(blank=False)
	podcast_url = models.TextField(blank=False)
	image = models.ImageField(blank=True)
	overall_goals = models.TextField(blank=True)
	learning_objective = models.TextField(blank=True)
	content_type = models.CharField(max_length=1, choices=type_choices, blank=False)
	duration = models.DurationField(blank=False)
	target_audience = models.CharField(max_length=250, blank=True)
	language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False)
	language_variety = models.CharField(max_length=150, blank=True)
	register = models.CharField(max_length=150, blank=True)
	accent = models.CharField(max_length=150, blank=True)
	language_features = models.CharField(max_length=250, blank=True)
	language_proficiency = models.CharField(max_length=150, blank=True)
	communication_mode = models.CharField(max_length=250, blank=True)
	commentary_available = models.BooleanField(default=False)
	instructor_produced = models.BooleanField(default=False)
	license = models.TextField(blank=True)
	captions_available = models.BooleanField(default=False)
	subtitles_language = models.CharField(max_length=150, blank=True)
	contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
	content_area = models.ForeignKey(Categories, on_delete=models.CASCADE)
	series = models.ForeignKey(Series, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tags, blank=True)
	created = models.DateTimeField(default=datetime.datetime.now)
	materials = models.ManyToManyField(Material, blank=True)

	def __str__(self):
		return str(self.title)