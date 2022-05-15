from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ('title', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)


class Post(models.Model, HitCountMixin):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=300, db_index=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish', db_index=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    video = models.FileField(upload_to='posts/%Y/%m/%d', blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish', )
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def current_hit_count(self):
        return self.hit_count.hits


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    # if you don't define related name attribute,
    # django will use 'name of model'_set (comment_set)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class Advertise(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='advertise/%Y/%m/%d', blank=True)
    body = models.TextField(max_length=500, blank=True)
    url = models.URLField(null=True)
    active = models.BooleanField(default=True)


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.BigIntegerField()
    message = models.TextField()
