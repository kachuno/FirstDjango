from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'MySite'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',
          auth_views.LoginView.as_view(template_name="MySite/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="MySite:login"), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('recipe_upload', views.recipe_upload, name='recipe_upload'),
    path('recipe_all/', views.recipe_all, name='recipe_all'),
    path('mypage/', views.mypage, name='mypage'),

    ### タイムライン ###
    path('post_all/', views.post_all, name='post_all'),
    path('post_all_user/', views.post_all_user, name='post_all_user'),
    path('upload/', views.post_create, name='post_create'),

    ### 管理者用 ###
    path('admin_page/', views.admin_page, name='admin_page'),

    ### スケジュール ###
    path('schedule_create/', views.schedule_create, name='schedule_create'),
    path('schedule_select/', views.schedule_select, name='schedule_select'),
    path('schedule_edit/<int:schedule_id>/', views.schedule_edit, name='schedule_edit'),
    path('schedule_delete/<int:schedule_id>/', views.schedule_delete, name='schedule_delete'),
    path('schedule_all/', views.schedule_all, name='schedule_all'),

    ### 各料理教室 ###
    path('lesson_detail/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson_create/', views.lesson_create, name='lesson_create'),
    path('lesson_edit/<int:lesson_id>/', views.lesson_edit, name='lesson_edit'),
    path('lesson_delete/<int:lesson_id>/', views.lesson_delete, name='lesson_delete'),

    ### お知らせ ###
    path('news_create/', views.news_create, name='news_create'),
    path('news_all/', views.news_all, name='news_all'),
    path('news_all_admin/', views.news_all_admin, name='news_all_admin'),
    path('news_edit/<int:news_id>/', views.news_edit, name='news_edit'),
    path('news_detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news_delete/<int:news_id>/', views.news_delete, name='news_delete'),

    ### レシピ ###
    path('recipe_all_admin/', views.recipe_all_admin, name='recipe_all_admin'),
    path('recipe_edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path('recipe_delete/<int:recipe_id>/', views.recipe_delete, name='recipe_delete'),

    ### ユーザ情報 ###
    path('user_all/', views.user_all, name='user_all'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
]
