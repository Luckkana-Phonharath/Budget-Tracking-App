"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from budget import views as budget_views
from django.conf.urls.static import static
from users import views as users_views
from social import views as social_views
from django.contrib.auth import views as authentication_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , budget_views.home, name='home'),
    path('register/', users_views.register, name='register'),
    path('login/' , authentication_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/' , authentication_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('profile/create', users_views.create_profile, name='create_profile'),
    path('search/', social_views.search_user, name='search_user'),
    path('profile/<str:username>/', users_views.profile_view, name='profile'),
    path('category/', budget_views.category, name='category'),
    path('category/add', budget_views.add_category, name='add_category'),
    path('category/edit/<int:category_id>/', budget_views.update_category, name='update_category'),
    path('category/delete/<int:id>/', budget_views.delete_category, name='delete_category'),
    path('allocate/', budget_views.allocate_budget, name='allocate_budget'),
    path('update-budget/<int:id>/', budget_views.update_budget, name='update_budget'),
    path('dashboard/', budget_views.dashboard, name='dashboard'),
    path('transactions/', budget_views.transaction_list, name='transaction_list'),
    path('transactions/add/', budget_views.add_transaction, name='add_transaction'),
    path('transactions/edit/<int:id>/', budget_views.edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:id>/', budget_views.delete_transaction, name='delete_transaction'),
    path('profile/<str:username>/', users_views.profile_view, name='profile'),
    path('send_friend_request/<str:username>/', social_views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<str:username>/', social_views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<str:username>/', social_views.reject_friend_request, name='reject_friend_request'),
    path('send_message/', social_views.send_message, name='send_message'),
    path('mark_message_read/<int:message_id>/', social_views.mark_message_read, name='mark_message_read'),
    path('profile/<str:username>/send-friend-request/', social_views.send_friend_request, name='send_friend_request'),
    path('profile/<str:username>/accept-friend-request/', social_views.accept_friend_request, name='accept_friend_request'),
    path('profile/<str:username>/reject-friend-request/', social_views.reject_friend_request, name='reject_friend_request'),
    path('report/', budget_views.report_view, name='report'),
    path('report_cv/', budget_views.report_view_cv, name='report_cv'),


]


urlpatterns += [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
