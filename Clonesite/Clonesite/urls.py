
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('account/login',views.LoginView.as_view(),name='login'),
    path('account/logout',views.LogoutView.as_view(),name='logout',kwargs={'next_page':'/'})
]
