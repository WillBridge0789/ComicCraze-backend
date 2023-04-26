import requests
import datetime
import hashlib
import environ

from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import *
from .serializers import *
env = environ.Env()

# Create your views here.
class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = UserWriteSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return UserWriteSerializer
        return UserReadSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ComicViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all()[:50]
    serializer_class = ComicSerializer

    def get_queryset(self):
        queryset = Comic.objects.all()
        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(title__icontains=q)
        return queryset

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all()
    serializer_class = WishlistSerializer

@method_decorator(csrf_exempt, name='dispatch')
def delete_favorite(request, user_id, comic_id):
    # fetch the object related to passed id
    user = get_object_or_404(CustomUser, pk=user_id)
    comic = get_object_or_404(Comic, pk=comic_id)
 
    if request.method == "DELETE":
        user.favorite_comics.remove(comic_id)
        return HttpResponse(status=204)


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


