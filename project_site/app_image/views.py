from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageForm
from .models import Image


def index(request):
    num_images = Image.objects.all().count()
    context = {
        'num_images': num_images,
    }
    return render(request, 'index.html', context=context)

def images(request):
    images = Image.objects.all()
    context = {
        'images' : images
    }
    return render(request, 'images.html', context=context)

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})
