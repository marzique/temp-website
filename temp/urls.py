from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Main page
    path('', include('main.urls')),
    
    # Team Players
    path('squad/', include('squad.urls')),

    # Scoreboard and matches
    path('scoreboard/', include('scoreboard.urls')),

    # Blog
    path('blog/', include('blog.urls')),

    # Forecasts
    path('forecasts/', include('forecasts.urls')),

    # Authentication
    path('auth/', include('users.urls')),
    path('account/', include('users.account_urls')),
    
    # enable the admin interface
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)