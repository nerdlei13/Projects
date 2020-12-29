"""web_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index1', views.index1, name='index1'),
    path('regular_output/', views.regular_output, name="regular_output"),
    path('admin_console/', views.admin_console, name="admin_console"),
    path('show_users/', views.show_users, name="show_users"),
    path('user_chart/', views.user_chart, name="user_chart"),
    path('advanced_output/', views.advanced_output, name="advanced_output"),
    path('demo_output/', views.demo_output, name="demo_output"),
    path('test/', views.test, name="test"),
    path('suggest_subreddit/', views.suggest_subreddit, name="suggest_subreddit"),
    path('show_history/', views.show_history, name="show_history"),
    path('show_advanced_history/', views.show_advanced_history,
         name="show_advanced_history"),
    path('crawl_demo/', views.crawl_demo, name="crawl_demo"),
    path('advanced_search/', views.advanced_search, name="advanced_search"),
    path('regular_search/', views.regular_search, name="regular_search"),
    path('search_subscribe/', views.search_subscribe, name="search_subscribe"),
    path('search_unsubscribe/', views.search_unsubscribe, name="search_unsubscribe"),
    path('advanced_search_subscribe/', views.advanced_search_subscribe, name="advanced_search_subscribe"),
    path('advanced_search_unsubscribe/', views.advanced_search_unsubscribe, name="advanced_search_unsubscribe"),
    path('search_subscription/', views.search_subscription, name="search_subscription"),
    path('pass_forgot/', views.pass_forgot, name="pass_forgot"),
    path('pass_change/', views.pass_change, name="pass_change"),
    path('pass_change_success/', views.pass_change_success,name="pass_change_success"),
    path('pass_found/', views.pass_found, name="pass_found"),
    path('register/', user_views.register, name="register"),
    path('check_username/', user_views.check_username, name="check_username"),
    path('check_email/', user_views.check_email, name="check_email"),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('login/', user_views.login_page, name='login'),
    path('topfiveusers/', views.topFiveUsers, name="topfiveusers"),
    path('topfivekeywords', views.topFiveKeyword, name='topfivekeywords'),
    path('top5keywords', views.top5keywords, name='top5keywords'),
    path('top5users/', views.top5users, name='top5users'),
    path('topfiveusers/', views.topFiveUsers, name='topfiveusers'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("password-reset", auth_views.PasswordResetView.as_view( template_name="users/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="users/password_reset_complete.html"), name="password_reset_complete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#views.subscription_background(repeat=10)
