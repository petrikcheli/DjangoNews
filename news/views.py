from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Post_Draft
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostSerializer, PostDraftSerializer

from django.db.models import QuerySet
from rest_framework import generics, permissions

from .forms import PostForm

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   
            post.save()
            return redirect('news:home_page')
    else:
        form = PostForm()

    return render(request, 'news/post/add_post.html', {'form': form})

#@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('no_access'))
# HTML 
@staff_member_required
def draft_list(request):
    posts = Post_Draft.objects.all()
    return render(request, 'news/post/draft_list.html', {'posts': posts})

class PostDraftCreateView(generics.CreateAPIView):
    serializer_class = PostDraftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDraftUpdateView(generics.UpdateAPIView):
    serializer_class = PostDraftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post_Draft]:
        return Post_Draft.objects.filter(author=self.request.user)


class PostDraftDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post_Draft]:
        return Post_Draft.objects.filter(author=self.request.user)

#Pub

class PostPubCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostPubUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(author=self.request.user)


class PostPubDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(author=self.request.user)


def post_list(request):
    posts = Post.published.all()
    return render(request, 'news/post/list.html', {'posts': posts})

def post_add(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'news/post/add_post.html', {'post': post})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'news/post/detail.html', {'post': post})


# API 

class PostListAPI(generics.ListAPIView):
    """
    GET: Получить список опубликованных постов
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

# Детали конкретного поста
class PostDetailAPI(generics.RetrieveAPIView):
    """
    GET: Получить конкретный опубликованный пост
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

@swagger_auto_schema(
    method='get',
    responses={200: PostSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def draft_list_api(request):
    drafts = Post.objects.filter(status=Post.Status.DRAFT)
    serializer = PostSerializer(drafts, many=True)
    return Response(serializer.data)