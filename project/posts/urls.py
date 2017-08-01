from django.conf.urls import url

from .views import (
	post_list,
	post_detail,
	post_create,
	post_edit,
	post_by_tag,
	tag_create,
	learn_more,
)

urlpatterns = [
	url(r'^$', post_list, name="post_list"),
	url(r'^more/$', learn_more, name="learn_more"),
	url(r'^(?P<id>[\d+])/$', post_detail, name="post_detail"),
	url(r'^create/$', post_create, name="post_create"),
	url(r'^(?P<id>[\d+])/edit/$', post_edit, name="post_edit"),
	url(r'^tag=(?P<tag>[\w-]+)/$', post_by_tag, name="post_by_tag"),
	url(r'^tag/create/$', tag_create, name="tag_create"),
]
