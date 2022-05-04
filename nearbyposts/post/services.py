from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import fromstr
from django.forms import modelform_factory, ModelForm, Textarea
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'longitude', 'latitude', 'tags', 'creator')
        widgets = {
            'content': Textarea(attrs={'rows': 3})
        }

def get_post_form(data: dict):
    if data:
        return PostForm(data)
    else:
        return PostForm()

def get_my_posts(username: str):
    return Post.objects.filter(creator=username).order_by('created_at')

def get_nearby_posts_within(latitude: float, longitude: float, 
        km: int=1, limit: int=None, srid: int=4326):
    coordinates = Point(longitude, latitude, srid=srid)
    point = GEOSGeometry(coordinates, srid=4326)
    return Post.objects.alias(distance=Distance('location', 
        coordinates)).filter(location__distance_lte=(point, 
        D(km=km))).order_by('distance')[0:limit]

def create_post(title: str, content: str, tags: list,
        longitude: str, latitude: str, creator: str):
    post = Post(
        title = title,
        content = content,
        tags = tags,
        longitude = longitude,
        latitude = latitude,
        creator = creator,
        location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
        )
    post.save()
    return post

