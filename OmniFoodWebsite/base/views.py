from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post


# Create your views here.
def home (request):
    context = { 
        'posts': Post.objects.all()
    }
    return render(request,'home.html',context)

@login_required
def recipes(request):
    return render(request,'recipes_home.html')