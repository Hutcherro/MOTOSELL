from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', views.mainView, name='main'),
    # path('img/', serve, name='main'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup/', views.main, name='signup'),
    path('<int:pk>/currentItem/', views.currentItem, name='currentItem'),
    path('accounts/login/', views.loginView, name='login'),
    path('accounts/signup/', views.signupView, name='signup'),
    path('accounts/logout/', views.logoutView, name='logout'),
    path('accounts/profile/', views.profileView, name='profile'),
    path('accounts/profile/addNotice/', views.createNoticeView, name='addNotice'),
    path('accounts/profile/addNotice/upload/', views.addNoticeView, name='uploadNotice'),
    path('accounts/profile/<int:pk>/updateForm/', views.updateForm, name='updateNoticeForm'),
    path('accounts/profile/<int:pk>/publicated/', views.publicated, name='publicateNotice'),
    path('accounts/profile/<int:pk>/update/', views.update_database, name='updateNotice'),
    path('accounts/profile/<int:pk>/delete/', views.delete, name='deleteNotice'),
    path('accounts/profile/<int:pk>/download/', views.download, name='downloadNotice'),
    # path('accounts/profile/password_change/', views.password_changeView, name='password_change'),
    # path('img/', include('motosell.img')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^img/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]