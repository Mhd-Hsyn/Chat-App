from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"userauth", UserAuthViewset, basename="userauth")
urlpatterns = [
    path("", include(router.urls)),
    path('chat/', ChatAPIView.as_view(), name= "chat"),
    path('message/', MessageAPIView.as_view(), name= "message"),
]
