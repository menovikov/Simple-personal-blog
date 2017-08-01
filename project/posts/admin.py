from django.contrib import admin
from .models import (
		Post, 
		Tag, 
		Profile, 
		WorkPlace, 
		SkillGroup, 
		SkillInstance,
		Subscriber,
	)


class PostModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'content', 'created', 'read_time', ]
	list_editable = ['title', 'content', 'read_time',]


class TagModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', ]
	list_editable = ['title', ]


class WorkplaceModelAdmin(admin.TabularInline):
	model = WorkPlace
	extra = 0


class SkillInstanceModelAdmin(admin.TabularInline):
	model = SkillInstance
	extra = 0


class SkillGroupModelAdmin(admin.ModelAdmin):
	list_display = ['title']
	inlines = [SkillInstanceModelAdmin, ]


class SkillGroupModelAdminInline(admin.TabularInline):
	model = SkillGroup
	extra = 0
		

class ProfileModelAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'occupation',
		'city',
		'welcome_phrase',
	]
	inlines = [
		WorkplaceModelAdmin,
		SkillGroupModelAdminInline,
	]


class SubscriberAdmin(admin.ModelAdmin):
	list_display = ['email_address', 'name', 'active']
	list_editable = ['active', 'name']
		

admin.site.register(Post, PostModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Profile, ProfileModelAdmin)
admin.site.register(SkillGroup, SkillGroupModelAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
