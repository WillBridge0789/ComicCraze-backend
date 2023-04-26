from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'comics', ComicViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('user/signup/', UserCreate.as_view(), name="create_user"),
    path('users/<int:pk>/', UserDetail.as_view(), name="get_user_details"),
    path('users/<int:user_id>/delete-favorite/<int:comic_id>/', delete_favorite),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]