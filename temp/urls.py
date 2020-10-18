from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    # comings soon TEMPORARY main page
    path('', include('comingsoon.urls')),

    path('squad/', include('squad.urls')),

    # provide the most basic login/logout functionality
    path('login/', auth_views.LoginView.as_view(template_name='auth/core/login.html'),
        name='core_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='core_logout'),

    # enable the admin interface
    path('admin/', admin.site.urls),
]
