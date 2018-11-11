from django.urls import path
from . import views
from django_registration.signals import user_registered

user_registered.connect(views.add_user_to_group_users)

urlpatterns = [

    path('', views.index, name='index'),

    path('blog/all', views.BlogListView.as_view(), name='blog-list'),
    path('blogger/all', views.BloggerListView.as_view(), name='blogger-list'),

    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),

    path('blog/create', views.BlogCreate.as_view(), name='blog-create'),
    path('blogger/create', views.BloggerCreate.as_view(), name='blogger-create'),

    path('comment/create/<int:pk>', views.CommentCreate.as_view(), name='comment-create'),
]
