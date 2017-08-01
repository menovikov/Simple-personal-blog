import logging
from django.db import transaction
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import (
	redirect, 
	render, 
	render_to_response,
	get_object_or_404
	)

from .models import (
	Post, 
	Tag,
	Profile,
	Subscriber,
	)
from .forms import (
	PostForm, 
	TagForm, 
	)

logger = logging.getLogger('filelogger')


""" Views """

def post_list(request):
	queryset = Post.objects.all()
	context = {
		'post_list' : queryset,
	}
	return render(request, 'post_list.html', context)


@transaction.atomic
def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	context = {
		'instance' : instance,
	}
	
	if request.method == 'POST':
		email_address = request.POST.get('name')
		if email_address != '' and len(email_address) < 100:
			try:
				Subscriber.objects.create(
					email_address=email_address
				)
			except Exception as e:
				logger.error(e)
	return render(request, 'post_detail.html', context)
	

@transaction.atomic
def post_edit(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, 
		request.FILES or None, instance=instance)
	context = {
		'instance' : instance,
		'form' : form,
	}
	if form.is_valid():
		instance = form.save()
		return redirect('post_detail', id=instance.id)
	return render(request, 'post_create.html', context)


@transaction.atomic
def post_create(request):
	if not request.user.is_authenticated():
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save()
		return redirect('post_list')
	context = {
		"form" : form,
	}
	return render(request, 'post_create.html', context)
	

def post_by_tag(request, tag=None):
	tag = get_object_or_404(Tag, title=tag)
	queryset = tag.blog.all()
	context = {
		'post_list' : queryset,
	}
	return render(request, 'post_list.html', context)


@transaction.atomic
def tag_create(request):
	if not request.user.is_authenticated():
		raise Http404
	form = TagForm(request.POST or None)
	context = {
		'form' : form,
	}
	if form.is_valid():
		instance = form.save()
		return redirect('post_list')
	return render(request, 'post_create.html', context)
	

def profile_view(request):
	context = {
		'profile' : Profile.objects.first()
	}
	return render(request, 'profile.html', context)
	

def learn_more(request):
	profile = Profile.objects.first()

	context = {
		'welcome_phrase' : profile.welcome_phrase,
		'email' : profile.email_address
	}
	if request.method == 'POST':
		email_address = request.POST.get('name')
		if email_address != '' and len(email_address) < 100:
			try:
				Subscriber.objects.create(
					email_address=email_address
				)
			except Exception as e:
				logger.error(e)
	return render(request, 'learn_more.html', context)


def redirect_view(request):
	return redirect('/blog/')


def handler404(request):
	# if (request.device.width > request.device.height):
	response = render_to_response('404.html', {},
								  context_instance=RequestContext(request))
	response.status_code = 404
	return response
