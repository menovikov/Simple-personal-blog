from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from markdown_deux import markdown


class Tag(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.title = self.title.lower()
		super(Tag, self).save(*args, **kwargs)

def img_upload_location(post, filename):
	return "%s/%s" %(post.id, filename)


class Post(models.Model):
	title = models.CharField(max_length=150)
	content = models.TextField()
	image = models.ImageField(
		upload_to=img_upload_location, 
		null=True, 
		blank=True,
		height_field='height_field', 
		width_field='width_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	draft = models.BooleanField(default=True)
	read_time = models.CharField(max_length=20, null=True, blank=True)
	tag = models.ManyToManyField(Tag, related_name='blog', blank=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

	def get_markdown(self):
		content = self.content
		return mark_safe(markdown(content))


@receiver(pre_save, sender=Post)
def CountReadTime(sender, instance, **kwargs):
	if instance is not None:
		content_length = len(instance.content)
		if content_length > 240:
			minutes = content_length//240
			if minutes > 15:
				minutes = 15
			if minutes == 1:
				instance.read_time = '~1 minute'
			else:
				instance.read_time = '~' + str(minutes) + ' minutes'
		elif content_length < 240:
			instance.read_time = 'less than 1 minute'

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" 
        					  % model.__name__)


class Profile(models.Model):
	# Common info
	name = models.CharField(max_length=50)
	occupation = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	email_address = models.EmailField(null=True)

	# Education
	university = models.CharField(max_length=150)
	faculty = models.CharField(max_length=100)
	grad_years = models.CharField(max_length=50)
	image = models.ImageField(
		upload_to='profile_img/', 
		null=True, 
		blank=True,
		height_field='height_field', 
		width_field='width_field')
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	welcome_phrase = models.TextField(null=True)

	def __str__(self):
		return self.name

	def clean(self):
		validate_only_one_instance(self)

	def get_workplaces(self):
		return WorkPlace.objects.filter(owner=self)

	def get_skill_groups(self):
		return SkillGroup.objects.all().order_by('order_id')


class WorkPlace(models.Model):
	company = models.CharField(max_length=50)
	project = models.CharField(max_length=100)
	corp_title = models.CharField(max_length=100)
	start_end_dates = models.CharField(max_length=50)
	description = models.TextField()
	order_id = models.IntegerField(default=0, unique=True)
	owner = models.ForeignKey(Profile, default=1)

	def get_markdown(self):
		content = self.description
		return mark_safe(markdown(content))


class SkillGroup(models.Model):
	title = models.CharField(max_length=50)
	order_id = models.IntegerField(default=0, unique=True)
	owner = models.ForeignKey(Profile, default=1)

	def get_related_skills(self):
		return SkillInstance.objects.filter(skill_group=self)


class SkillInstance(models.Model):
	title = models.CharField(max_length=75)
	level = models.CharField(max_length=50)
	experience_time = models.CharField(max_length=50)
	skill_group = models.ForeignKey(SkillGroup, blank=True, null=True)

	def __str__(self):
		return "%s  -  %s  -  %s" %(self.title, self.level, 
									self.experience_time)


class Subscriber(models.Model):
	email_address = models.EmailField()
	name = models.CharField(max_length=100, blank=True, null=True)
	active = models.BooleanField(default=True, blank=True)


pre_save.connect(CountReadTime, sender=Post)
