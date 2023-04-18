from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.http import JsonResponse
import requests
import datetime
import hashlib
import environ
env = environ.Env()

# Create your views here.
class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



# def api_data_view(request):
#     data = get_data_from_api()
#     return JsonResponse(data)

def get_comic(request):
  timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
  pub_key = env("MARVEL_PUB")
  priv_key = env("MARVEL_PRIV")

  def hash_params():
      """ Marvel API requires server side API calls to include
      md5 hash of timestamp + public key + private key """

      hash_md5 = hashlib.md5()
      hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
      hashed_params = hash_md5.hexdigest()

      return hashed_params

  # Could be some other paramaters to send to get a better list of comics. 
  # https://developer.marvel.com/docs#!/public/getComicsCollection_get_6
  params = {
    'ts': timestamp,
    'apikey': pub_key,
    'hash': hash_params(),
    'limit': 100,
    'orderBy': 'onsaleDate',
  }

  res = requests.get(
    'https://gateway.marvel.com:443/v1/public/comics/9871',
    params=params,
    headers={'Content-Type': 'application/json'}
  )
  comic = res.json()
  return JsonResponse(comic)


