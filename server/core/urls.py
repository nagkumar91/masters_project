from django.conf.urls import url, include
from .api import router
from .views import CreateUser, request_ride, login_appuser

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'create_user/', CreateUser.as_view(), name="create_user"),
    url(r'request_ride/', request_ride, name="request_ride"),
    url(r'login/', login_appuser, name="login_appuser"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
