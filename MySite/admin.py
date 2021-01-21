from django.contrib import admin
from .models import Schedule, Post, Recipe, LessonSchedule, News, Comment
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(Schedule)
admin.site.register(Post)
admin.site.register(Recipe)
admin.site.register(LessonSchedule)
admin.site.register(News)
admin.site.register(Comment)
