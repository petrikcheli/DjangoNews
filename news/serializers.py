from rest_framework import serializers
from .models import Post, Post_Draft

class PostDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Draft
        fields = ['id', 'title', 'slug', 'body', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField() 

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'publish', 'created', 'updated', 'status', 'author']