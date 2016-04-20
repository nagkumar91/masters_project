from django.conf.urls import patterns, url, include
from .api import router
from .views import CreateUser, get_token

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'create_user/', CreateUser.as_view(), name="create_user"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
