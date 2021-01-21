from django import forms
from . import models
from django.contrib.auth.models import User
from .models import Post, Recipe, Schedule, LessonSchedule, News

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    enter_password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username has been already taken.')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('Password must contain 5 or more characters.')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'This does not match with the above.')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        new_user = User.objects.create_user(username = username, password=password)
        new_user.set_password(password)
        new_user.save()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','picture']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('holdmonth','description', 'document')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['holdmonth','theme','members','picture1','picture2','picture3','now']

class ScheduleSelectForm(forms.Form):
    choice = forms.ModelChoiceField(models.Schedule.objects.order_by('-holdmonth'), label='開催年月', empty_label='選択してください')

class LessonForm(forms.ModelForm):
    class Meta:
        model = LessonSchedule
        fields = ['holdmonth','date','members']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title','message','contents','created_at']
