from django.conf import settings
from django.shortcuts import render
from rest_framework import mixins, generics
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AppUser
from .serializers import CreateUserSerializer

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CreateUser(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_token(request):
    return Response({"Token": settings.DEFAULT_TOKEN}, status=status.HTTP_200_OK)
