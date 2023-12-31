# RiffMates/RiffMates/urls.py
from django.contrib import admin
from django.urls import include, path
from home import views as home_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home_views.home, name="home"),
    path("credits/", home_views.credits, name="credits"),
    path("about/", home_views.about),
    path("version/", home_views.version),
    path("news/", home_views.news, name="news"),
    path("adv_news/", home_views.news_advanced, name="adv_news"),
    path("bands/", include("bands.urls")),
    path("content/", include("content.urls")),
]
