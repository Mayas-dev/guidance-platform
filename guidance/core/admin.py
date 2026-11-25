from django.contrib import admin
from .models import Topic, UserTopic, Profile,  GuidanceRequest

admin.site.register(Topic)
admin.site.register(UserTopic)
admin.site.register(Profile)
admin.site.register(GuidanceRequest)