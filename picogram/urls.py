from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from user import views as user_views
from django.contrib.auth import views as auth_views
from post.views import ExploreListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('explore/', ExploreListView.as_view(), name='explore'),

    path('user/<int:pk>', user_views.u_profile, name='u-profile'),
    path('user/<int:pk>/follow', user_views.follow_user, name='follow'),
    path('user/<int:pk>/unfollow', user_views.unfollow_user, name='unfollow'),
    path('register/', user_views.register, name='register'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html",
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html'),
         name='password_reset'
         ),


    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'),
         name='password_reset_complete'
         ),


    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'),
         name='password_reset_done'
         ),

    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('', include("post.urls"))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
