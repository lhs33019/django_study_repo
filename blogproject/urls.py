from django.contrib import admin
from django.urls import path, include
import blogapp.views
import portfolioapp.views
import accounts.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogapp.views.home, name="home"),
    path('blog/', include('blogapp.urls')),
    path('portfolio', portfolioapp.views.portfolio, name="portfolio"),
    path('accounts/', include('accounts.urls')),
    path('get/moviechart', blogapp.views.movieChart, name='movieChart'),
    path('test/posting', blogapp.views.makeTestPosts, name='makeTestPosts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)