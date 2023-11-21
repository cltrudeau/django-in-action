# RiffMates/RiffMates/urls.py
from bands.api import router as bands_router
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from home import views as home_views
from home.api import router as home_router
from ninja import NinjaAPI
from promoters.api import router as promoters_router

api = NinjaAPI(version="1.0")
api.add_router("/home/", home_router)
api.add_router("/promoters/", promoters_router)
api.add_router("/bands/", bands_router)

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
    path("api/v1/", api.urls),
    path("promoters/", include("promoters.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
