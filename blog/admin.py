from django.contrib import admin
from .models import Post, Category, Advertise, Comment, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'image', 'video',
                    'author', 'created', 'publish',
                    'updated', 'current_hit_count')

    list_filter = ('category', 'author', 'author', 'publish', 'updated')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'body', 'active', 'created', 'updated')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    # update state of all chosen comments to active at once
    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'url', 'active')
    list_filter = ('active',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
