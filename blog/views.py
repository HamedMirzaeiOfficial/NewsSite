from django.shortcuts import render, reverse, redirect
from .models import Post, Advertise, Category, Contact
from django.shortcuts import get_object_or_404
from hitcount.views import HitCountDetailView
from django.views.generic import ListView, DetailView, View
from django.db.models import Count, Q
from .forms import CommentForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, FormView
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin


class HomePageView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.published.all()[0:8]
        context['categories'] = Category.objects.all().annotate(num_posts=Count('posts')).order_by('-num_posts')
        context['advertises'] = Advertise.objects.filter(active=True)[:3]
        context['videos'] = Post.published.exclude(video__exact='').order_by('-hit_count_generic__hits')[1:4]
        context['most_viewed_post'] = Post.published.filter(video__exact='').order_by('-hit_count_generic__hits').first()
        context['most_viewed_posts'] = Post.published.filter(video__exact='').order_by('-hit_count_generic__hits')[1:4]
        context['most_viewed_video'] = Post.published.exclude(video__exact='').order_by('-hit_count_generic__hits').first()
        return context


class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostDisplay(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        success_message = 'کامنت شما فرستاده شد.'
        messages.success(self.request, success_message)
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug}) + '#comments'


class PostListByCategory(ListView):
    model = Post
    template_name = 'blog/post_list_by_category.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['slug'])


class PostCountHitDetailView(HitCountDetailView):
    model = Post
    count_hit = True


class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm

    def get_success_url(self):
        success_message = 'پیام شما برای ادمین فرستاده شد.'
        messages.success(self.request, success_message)
        return reverse('contact')


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data(*args, **kwargs)
        context['search_word'] = self.request.GET.get('q')
        return context
