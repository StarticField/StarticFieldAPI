from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', RoomView.as_view()),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', UserRegistrationView.as_view(), name="create_user"),
    path('cto-hunt/registration/', CTOHuntRegistrationView.as_view(), name="cto_hunt_registration")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)