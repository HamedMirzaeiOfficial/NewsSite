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


# def index(request):
#     posts = Post.published.all()[:8]
#     categories = Category.objects.all().annotate(num_posts=Count('posts')).order_by('-num_posts')
#     advertises = Advertise.objects.filter(active=True)[:3]
#     videos = Post.published.exclude(video__exact='')[:4]
#     most_viewed_post = Post.published.filter(video__exact='').order_by('-hit_count_generic__hits').first()
#     most_viewed_posts = Post.published.filter(video__exact='').order_by('-hit_count_generic__hits')[1:4]
#     most_viewed_video = Post.published.exclude(video__exact='').order_by('-hit_count_generic__hits').first()
#     return render(request, 'index.html',
#                   {'posts': posts, 'advertises': advertises, 'categories': categories,
#                    'most_viewed_posts': most_viewed_posts, 'most_viewed_post': most_viewed_post,
#                    'videos': videos, 'most_viewed_video': most_viewed_video})
#
#
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
        messages.success(self.request, 'کامنت شما فرستاده شد.')
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug}) + '#comments'


# def post_detail(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     comments = post.comments.filter(active=True)
#     paginator = Paginator(comments, 5)
#     page = request.GET.get('page')
#     try:
#         comments = paginator.page(page)
#     except PageNotAnInteger:
#         # if page is not an integer, deliver the first page
#         comments = paginator.page(1)
#     except EmptyPage:
#         # if pag is out of range, deliver last page of results
#         comments = paginator.page(paginator.num_pages)
#
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#
#     return render(request, 'blog/post_detail.html',
#                   {'post': post, 'comments': comments,
#                    'new_comment': new_comment, 'comment_form': comment_form})


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


# def post_list_by_category(request, category_slug):
#     category = Category.objects.get(slug=category_slug)
#     posts = Post.published.filter(category=category)
#     paginator = Paginator(posts, 8)  # 12 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # if page is not an integer, deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # if pag is out of range, deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post_list_by_category.html',
#                   {'posts': posts, 'category': category})
#

class PostCountHitDetailView(HitCountDetailView):
    model = Post
    count_hit = True


class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm

    def get_success_url(self):
        messages.success(self.request, 'پیام شما برای ادمین فرستاده شد.')
        return reverse('contact')


# def contact(request):
#     message = None
#     if request.method == 'POST':
#         message_form = ContactForm(data=request.POST)
#         if message_form.is_valid():
#             message = message_form.save()
#     else:
#         message_form = ContactForm()
#
#     return render(request, 'blog/contact.html',
#                   {'message_form': message_form})


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
