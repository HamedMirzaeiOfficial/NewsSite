from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('category', views.CategoryViewSet, basename='categories')
router.register('posts', views.PostViewSet, basename='posts')
urlpatterns = router.urls
