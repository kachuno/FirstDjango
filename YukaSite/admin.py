from django.contrib import admin
from .models import Schedule, Post, Recipe, LessonSchedule, News
from django.contrib.auth.admin import UserAdmin
#, LessonGroup, LessonMember
from .models import User

admin.site.register(Schedule)
admin.site.register(Post)
admin.site.register(Recipe)
admin.site.register(LessonSchedule)
admin.site.register(News)
