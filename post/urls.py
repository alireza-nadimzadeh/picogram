from .views import unlike, like, ExploreListView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.urls import path, include
from . import views
from picogram import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', PostListView.as_view(), name='home'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/unlike', unlike, name='unlike'),
    path('post/<int:pk>/like', like, name='like'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
