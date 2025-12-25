from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # HTML
    path('', views.post_list, name='home_page'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('drafts/', views.draft_list, name='draft_list'),

    path('posts/create/', views.post_create_view, name='post_create'),

    # API
    path('api/posts/', views.PostListAPI.as_view(), name='api_post_list'),
    path('api/posts/<int:id>/', views.PostDetailAPI.as_view(), name='api_post_detail'),
    path('api/posts/drafts/', views.draft_list_api, name='api_draft_list'),


    path('drafts/create/', views.PostDraftCreateView.as_view()),
    path('drafts/<int:pk>/delete/', views.PostDraftDeleteView.as_view()),
    path('drafts/<int:pk>/edit/', views.PostDraftUpdateView.as_view()),

    path('pubs/create/', views.PostPubCreateView.as_view()),
    path('pubs/<int:pk>/delete/', views.PostPubDeleteView.as_view()),
    path('pubs/<int:pk>/edit/', views.PostPubUpdateView.as_view()),
]
