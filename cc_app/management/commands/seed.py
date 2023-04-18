from django.http import JsonResponse
from django.core.management.base import BaseCommand
import requests
import datetime
import hashlib
import environ
from ...models import Comic
env = environ.Env()

def get_comic():
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
    'offset': 40000
  }

  res = requests.get(
    'https://gateway.marvel.com:443/v1/public/comics',
    params=params,
    headers={'Content-Type': 'application/json'}
  )
  data = res.json()
  return data["data"]["results"]

def add_comics_to_db():
  for i in get_comic():
    # Where you will add fields from the json response to save to the db model fields.
    comic = Comic(
      title=i["title"],
    )
    comic.save()

def clear_data():
  Comic.objects.all().delete()


class Command(BaseCommand):
  def handle(self, *args, **options):
    add_comics_to_db()
    # clear_data()
    print("completed")