from django.shortcuts import render

# Create your views here.
from .models import Shorts

def movie_shorts(request):
    shorts = Shorts.objects.filter(comment_star__gt=3)
    return render(request, 'result.html', locals())