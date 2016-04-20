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
from .serializers import CreateUserSerializer, RideRequestSerializer

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CreateUser(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = CreateUserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['POST'])
def request_ride(request):
    if request.user:
        request_payload = request.data
        request_payload['requested_by'] = request.user.pk
        serailizer = RideRequestSerializer(data=request_payload)
        if serailizer.is_valid():
            serailizer.save()
            return Response({"saved": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": True, "message": "No auth token provided"}, status=status.HTTP_401_UNAUTHORIZED)
