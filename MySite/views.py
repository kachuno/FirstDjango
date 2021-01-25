from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
from .models import Schedule, Post, Recipe
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import *
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.
# サインアップ用
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MySite:index')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'MySite/signup.html', context)

##トップページ
@login_required
def index(request):
    login_user_id = request.user.id
    data = Schedule.objects.all().filter(now=True)
    params = {'message': '教室スケジュール', 'data': data}
    return render(request, 'MySite/index.html', params)

##投稿一覧
@login_required
def post_all(request):
    user_me = request.user.id
    posts = Post.objects.all().order_by('-pub_date')[0:15]
    params = {'message':'投稿一覧', 'posts': posts,'user_me':user_me}
    return render(request, 'MySite/post.html', params)

##投稿一覧（ユーザー用）
@login_required
def post_all_user(request):
    user = request.user.id
    posts = Post.objects.all().filter(owner=user).order_by('-pub_date')[0:15]
    params = {'posts':posts,'user':user}
    return render(request, 'MySite/post_all_user.html', params)

##新規投稿
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('MySite:post_all')
    else:
        form = PostForm()

    context = {'form':form}
    return render(request, 'MySite/post_create.html', context)

##投稿詳細
@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        models.Comment.objects.create(text=request.POST["text"],post=post)

    return render(request, 'MySite/post_detail.html', {'post': post})

##レシピアップロード
@login_required
def recipe_upload(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('MySite:admin_page')
    else:
        form = RecipeForm()
    return render(request, 'MySite/recipe_upload.html', {
        'form': form
    })

##レシピ一覧
@login_required
def recipe_all(request):
    login_user_id = request.user.id
    whose_list = Schedule.objects.filter(members__in=User.objects.filter(id=login_user_id))
    recipes = Recipe.objects.filter(holdmonth__in=whose_list).order_by('holdmonth').reverse()
    params = {'id':login_user_id, 'who':whose_list, 'recipes': recipes}
    return render(request, 'MySite/recipe_all.html', params)

##マイページ
@login_required
def mypage(request):
    login_user_id = request.user.id
    who = User.objects.filter(id=login_user_id)
    data = Schedule.objects.filter(members__in=who).order_by('holdmonth').reverse()
    whose_list = Schedule.objects.filter(members__in=User.objects.filter(id=login_user_id))
    lessons = LessonSchedule.objects.filter(members__in=User.objects.filter(id=login_user_id))
    recipes = Recipe.objects.filter(holdmonth__in=whose_list)
    post = Post.objects.filter(owner__in=who).all().order_by('pub_date').reverse()
    params = {'id':login_user_id,'who':who,'data':data,'recipes':recipes,'lessons':lessons,'post':post}
    return render(request, 'MySite/mypage.html',params)

##スケジュールの登録
def schedule_create(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #今月のテーマに適用する場合，他のテーマのチェックを外す
            nowor = request.POST.get('now')
            if nowor == 'on':
                before_now = Schedule.objects.all().filter(now=True).first()
                before_now.now = False
                before_now.save(update_fields=['now'])
            else:
                before_now = 'hello'
            data = Schedule.objects.all().filter(now=True).last()
            lessons = LessonSchedule.objects.filter(holdmonth=data)
            recipes = Recipe.objects.filter(holdmonth=data)
            params = {'message': '教室スケジュール', 'data': data, 'lessons': lessons,'recipes':recipes}
            return render(request, 'MySite/admin_page.html',params)
    else:
        form = ScheduleForm()

    context = {'form':form}
    return render(request, 'MySite/schedule_create.html', context)

##スケジュールの更新
def schedule_edit(request, schedule_id):
    obj = Schedule.objects.get(id=schedule_id)
    if request.method == "POST":
        form = ScheduleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            data = Schedule.objects.all().order_by('holdmonth').reverse()
            params = {'message': '教室スケジュール', 'data': data}
            return render(request, 'MySite/schedule_all.html',params)
    else:
        form = ScheduleForm(instance=obj)

    context = {'form':form, 'id':schedule_id}
    return render(request, 'MySite/schedule_edit.html', context)

##スケジュールの削除
def schedule_delete(request, schedule_id):
    obj = Schedule.objects.get(id=schedule_id)
    forms = ScheduleSelectForm(request.POST, request.FILES)
    if(request.method == 'POST'):
        obj.delete()
        data = Schedule.objects.all().filter(now=True).last()
        lessons = LessonSchedule.objects.filter(holdmonth=data)
        recipes = Recipe.objects.filter(holdmonth=data)
        params = {'data': data, 'lessons': lessons,'recipes':recipes,'form':forms}
        return render(request, 'MySite/admin_page.html',params)

    context = {'id':schedule_id,'schedule':obj}
    return render(request, 'MySite/schedule_delete.html', context)

##今月のテーマの選択
def schedule_select(request):
    if request.method == "POST":
        form = ScheduleSelectForm(request.POST)
        if form.is_valid():
            selected_schedule = form.cleaned_data.get('choice')
            data = Schedule.objects.all().filter(holdmonth=selected_schedule).last()
            lessons = LessonSchedule.objects.filter(holdmonth=data)
            recipes = Recipe.objects.filter(holdmonth=data)
            #他のテーマのチェックを外す
            if Schedule.objects.all().filter(now=True).exists():
                before_now = Schedule.objects.all().filter(now=True).last()
                before_now.now = False
                before_now.save(update_fields=['now'])
            else:
                pass
            data.now = True
            data.save(update_fields=['now'])
            params = {'message': '教室スケジュール', 'data': data, 'lessons': lessons,'recipes':recipes}
            return render(request, 'MySite/admin_page.html', params)
    else:
        form = ScheduleSelectForm()
    context = {'form':form}
    return render(request, 'MySite/schedule_select.html', context)

##スケジュール一覧
def schedule_all(request):
    data = Schedule.objects.all().order_by('holdmonth').reverse()
    recipes = Recipe.objects.all()
    params = {'data': data, 'recipes':recipes}
    return render(request, 'MySite/schedule_all.html', params)

##管理用ページ
def admin_page(request):
    #管理者以外
    if not request.user.is_superuser:
        return redirect('MySite:index')

    data = Schedule.objects.all().filter(now=True).last()
    lessons = LessonSchedule.objects.filter(holdmonth=data)
    recipes = Recipe.objects.filter(holdmonth=data)

    #スケジュールの変更用
    if request.method == "POST":
        form = ScheduleSelectForm(request.POST)
        if form.is_valid():
            selected_schedule = form.cleaned_data.get('choice')
            data = Schedule.objects.all().filter(holdmonth=selected_schedule).last()
            lessons = LessonSchedule.objects.filter(holdmonth=data)
            recipes = Recipe.objects.filter(holdmonth=data)
            #他のテーマのチェックを外す
            if Schedule.objects.all().filter(now=True).exists():
                before_now = Schedule.objects.all().filter(now=True).last()
                before_now.now = False
                before_now.save(update_fields=['now'])
            else:
                pass
            data.now = True
            #msg ='ifに入らない'
            data.save(update_fields=['now'])
            params = {'message': '教室スケジュール', 'data': data, 'lessons': lessons,'recipes':recipes,'form':form}
            return render(request, 'MySite/admin_page.html', params)
    else:
        form = ScheduleSelectForm()

    params = {'message': '教室スケジュール', 'data': data, 'lessons': lessons,'recipes':recipes,'form':form}
    return render(request, 'MySite/admin_page.html', params)

##各教室詳細
def lesson_detail(request, lesson_id):
    lesson = LessonSchedule.objects.get(id=lesson_id)
    holdmonth = LessonSchedule.objects.filter(holdmonth=lesson.holdmonth)
    params ={'lesson': lesson}
    return render(request, 'MySite/lesson_detail.html', params)

##教室新規登録
def lesson_create(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            ## Lesson と Schedule のメンバーを紐付ける実装（未）
            #sch = Schedule.objects.get(holdmonth=post.holdmonth)
            #sch.members.set(post.members.all())
            #sch.save()
            form.save_m2m()
            return redirect('MySite:admin_page')
    else:
        form = LessonForm()
    context = {'form':form}
    return render(request, 'MySite/lesson_create.html', context)

##教室の更新
def lesson_edit(request, lesson_id):
    obj = LessonSchedule.objects.get(id=lesson_id)
    forms = ScheduleSelectForm(request.POST)
    if request.method == "POST":
        form = LessonForm(request.POST, instance=obj)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            data = Schedule.objects.all().filter(now=True).last()
            lessons = LessonSchedule.objects.filter(holdmonth=data)
            recipes = Recipe.objects.filter(holdmonth=data)
            params = {'data': data, 'lessons': lessons,'recipes':recipes,'form':forms}
            return render(request, 'MySite/admin_page.html',params)
    else:
        form = LessonForm(instance=obj)

    context = {'form':form, 'id':lesson_id}
    return render(request, 'MySite/lesson_edit.html', context)

##教室の削除
def lesson_delete(request, lesson_id):
    obj = LessonSchedule.objects.get(id=lesson_id)
    forms = ScheduleSelectForm(request.POST)
    if(request.method == 'POST'):
        obj.delete()
        data = Schedule.objects.all().filter(now=True).last()
        lessons = LessonSchedule.objects.filter(holdmonth=data)
        recipes = Recipe.objects.filter(holdmonth=data)
        params = {'data': data, 'lessons': lessons,'recipes':recipes,'form':forms}
        return render(request, 'MySite/admin_page.html',params)

    context = {'id':lesson_id,'lesson':obj}
    return render(request, 'MySite/lesson_delete.html', context)

##お知らせ登録
def news_create(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            data = News.objects.all().order_by('created_at').reverse()
            params = {'data': data}
            return render(request, 'MySite/news_all_admin.html', params)
    else:
        form = NewsForm()

    context = {'form':form}
    return render(request, 'MySite/news_create.html', context)

##お知らせ一覧
@login_required
def news_all(request):
    data = News.objects.all().order_by('created_at').reverse()
    params = {'data': data}
    return render(request, 'MySite/news_all.html', params)

##お知らせ一覧（管理者用）
def news_all_admin(request):
    data = News.objects.all().order_by('created_at').reverse()
    params = {'data': data}
    return render(request, 'MySite/news_all_admin.html', params)

##お知らせ更新
def news_edit(request, news_id):
    obj = News.objects.get(id=news_id)
    if request.method == "POST":
        form = NewsForm(request.POST, instance=obj)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            data = News.objects.all().order_by('created_at').reverse()
            params = {'data': data}
            return render(request, 'MySite/news_all_admin.html',params)
    else:
        form = NewsForm(instance=obj)

    context = {'form':form, 'id':news_id}
    return render(request, 'MySite/news_edit.html', context)

##お知らせの削除
def news_delete(request, news_id):
    obj = News.objects.get(id=news_id)
    if(request.method == 'POST'):
        obj.delete()
        data = News.objects.all().order_by('created_at').reverse()
        params = {'data': data}
        return render(request, 'MySite/news_all_admin.html',params)

    context = {'id':news_id,'news':obj}
    return render(request, 'MySite/news_delete.html', context)

##お知らせ詳細
@login_required
def news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'MySite/news_detail.html', {'news': news })

##レシピ一覧（管理者用）
def recipe_all_admin(request):
    data = Recipe.objects.all().order_by('holdmonth').reverse()
    params = {'data': data}
    return render(request, 'MySite/recipe_all_admin.html', params)

##レシピ更新
def recipe_edit(request, recipe_id):
    obj = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=obj)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            data = Recipe.objects.all().order_by('holdmonth').reverse()
            params = {'data': data}
            return render(request, 'MySite/recipe_all_admin.html', params)
    else:
        form = RecipeForm(instance=obj)

    context = {'form':form, 'id':recipe_id}
    return render(request, 'MySite/recipe_edit.html', context)

##レシピの削除
def recipe_delete(request, recipe_id):
    obj = Recipe.objects.get(id=recipe_id)
    if(request.method == 'POST'):
        obj.delete()
        data = Recipe.objects.all().order_by('holdmonth').reverse()
        params = {'data': data}
        return render(request, 'MySite/recipe_all_admin.html',params)

    context = {'id':recipe_id,'recipe':obj}
    return render(request, 'MySite/recipe_delete.html', context)

##ユーザー　一覧
def user_all(request):
    data = User.objects.all()
    params = {'data': data}
    return render(request, 'MySite/user_all.html', params)

##ユーザー情報詳細
def user_detail(request, user_id):
    login_user_id = request.user.id
    who = User.objects.filter(id=login_user_id)
    user = User.objects.get(id=user_id)
    users = User.objects.filter(id=user_id)
    data = Schedule.objects.filter(members__in=users).order_by('holdmonth').reverse()
    post = Post.objects.filter(owner__in=users).all().order_by('pub_date').reverse()
    params = {'user': user, 'data':data, 'post':post,'who':who}
    return render(request, 'MySite/user_detail.html', params)
