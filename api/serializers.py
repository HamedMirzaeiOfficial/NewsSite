from blog.models import Post, Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'image', 
                  'video', 'body', 'author', 'publish', 
                  'created', 'updated', 'status')
        
        