"""
URL configuration for ticket_notification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from musical.views import MusicalListView, PopularMusicalListView, UpcomingMusicalListView, CategoryListView, \
    GenreListView, MainImageListView, MusicalDetailView, signup, user_login, DemoMainPageView, DemoMusicalDetailView, \
    CategoryMusicalListView, DemoMyPageView, NoticeListView, NoticeDetailView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('musicals/popular/', PopularMusicalListView.as_view(), name="popular-musical-list"),
    path('musicals/upcoming/', UpcomingMusicalListView.as_view(), name="upcoming-musical-list"),
    path('categories/', CategoryListView.as_view(), name="category-list"),
    path('categories/<int:category_id>/musicals/', CategoryMusicalListView.as_view(), name='category-musical-list'),
    path('genres/', GenreListView.as_view(), name="genre-list"),
    path('main/images/', MainImageListView.as_view(), name="main-image-list"),
    path('musicals/<int:musical_id>/', MusicalDetailView.as_view(), name='musical_detail'),
    path('musicals/detail/<int:musical_id>/', DemoMusicalDetailView.as_view(), name='musical_detail'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', DemoMainPageView.as_view(), name='main-page'),
    path('mypage/', DemoMyPageView.as_view(), name='mypage'),
    path('musicals/detail/<int:musical_id>/', DemoMusicalDetailView.as_view(), name='musical_detail_demo'),
    path('notices/', NoticeListView.as_view(), name='notice-list'),
    path('notices/<int:notice_id>/', NoticeDetailView.as_view(), name='notice_detail'),



]
