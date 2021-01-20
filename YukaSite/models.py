import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Schedule(models.Model):
    """スケジュール"""
    holdmonth = models.CharField('開催年月', max_length=50, help_text="○年○月", default="2021年1月", unique=True)
    theme = models.TextField('テーマ', max_length=50, default="テスト")
    now = models.BooleanField('現在のテーマを選択',default=False)
    members = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    picture1 = models.ImageField(upload_to='images/',blank=True)
    picture2 = models.ImageField(upload_to='images/',blank=True)
    picture3 = models.ImageField(upload_to='images/',blank=True)

    def __str__(self):
        return self.holdmonth

class Post(models.Model):
    """投稿"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default='test',max_length=30)
    content = models.TextField(max_length=500)
    good_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images/')

    def __str(self):
        return str(self.content)
    ##投稿最新順
    class Meta:
        ordering = ('-pub_date',)

class Comment(models.Model):
    """投稿へのコメント"""
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Recipe(models.Model):
    """レシピ"""
    holdmonth = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    description = models.CharField(max_length=200,blank=True)
    document = models.FileField(upload_to='recipes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description

class LessonSchedule(models.Model):
    """Schedule内の各教室スケジュール"""
    holdmonth = models.ForeignKey(Schedule, related_name="lesson_month", on_delete=models.CASCADE)
    date = models.DateField('日付',unique=True)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.date)

class News(models.Model):
    """お知らせ"""
    title = models.CharField('タイトル', max_length=50, unique=True)
    message = models.TextField('お知らせ概要', max_length=200)
    contents = models.TextField('内容', max_length=500)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return str(self.title)
