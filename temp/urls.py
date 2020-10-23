from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # comings soon TEMPORARY main page
    # path('', include('comingsoon.urls')),

    # Main page
    path('', include('main.urls')),
    
    # Team
    path('squad/', include('squad.urls')),

    # Scoreboard
    path('scoreboard/', include('scoreboard.urls')),

    # Blog
    path('blog/', include('blog.urls')),

    # provide the most basic login/logout functionality
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # enable the admin interface
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)