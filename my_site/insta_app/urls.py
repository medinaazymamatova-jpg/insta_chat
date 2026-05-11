from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'follow', FollowViewSet),
router.register(r'hashtag', HashtagViewSet),
router.register(r'content', ContentViewSet),
router.register(r'post_like', PostLikeViewSet),
router.register(r'comment', CommentViewSet),
router.register(r'comment_like', CommentLikeViewSet),
router.register(r'save_post', SavePostViewSet),
router.register(r'save_post_item', SavePostItemViewSet),
router.register(r'stories', StoriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('post/', PostListApiView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailApiView.as_view(), name='post_detail'),

]




