from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterView, UserView, AdminViewSet, get_token
from reviews.views import ReviewViewSet, CommentViewSet
from categories.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = SimpleRouter()
router.register(r'users', AdminViewSet, basename='users')

router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)' r'/comments',
    CommentViewSet,
    basename='comments',
)
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/auth/token/', get_token, name='get_token'),
    path(
        'v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('v1/auth/signup/', RegisterView.as_view(), name='auth_register'),
    path('v1/users/me/', UserView.as_view(), name='user_me'),
    path('v1/', include(router.urls)),
]
