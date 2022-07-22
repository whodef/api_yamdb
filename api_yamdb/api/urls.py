from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AdminViewSet, RegisterView, UserView, get_token
from reviews.views import ReviewViewSet, CommentViewSet


router = SimpleRouter()  # Замена на SimpleRouter
router.register('users', AdminViewSet)

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

