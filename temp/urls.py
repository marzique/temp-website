from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import PrivacyPolicyView


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

    # privacy policy
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),

    # CKEditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # Telegram
    path('telegram/', include('telega.urls')),
    
    # backups
    path('admin/', include('smuggler.urls')),  # before admin url patterns!
    # enable the admin interface
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
