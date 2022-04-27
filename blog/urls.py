from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.PostListByCategory.as_view(), name='post_list_by_category'),

]
