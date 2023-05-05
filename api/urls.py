from django.urls import path, include

from rest_framework import routers
from .views import LoginUserApi, NewsPostView, CategoryView, TagsView, UserNewsPostRelationView, UserSubscriptionView, RegisterUserView

router = routers.DefaultRouter()
router.register('news', NewsPostView)
router.register('categories', CategoryView)
router.register('tags', TagsView)
router.register('UserRelation', UserNewsPostRelationView)
router.register('subscriptions', UserSubscriptionView)

urlpatterns = [
    path('login/', LoginUserApi.as_view(), name="login"),
    path('register', RegisterUserView.as_view(), name="register"),
    path('', include(router.urls))
]