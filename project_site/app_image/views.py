from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageForm
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import GeneratedImageForm
import requests
from io import BytesIO


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

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            form.save()
            return redirect('upload_image')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


class UploadedImagesByUserListView(LoginRequiredMixin, generic.ListView):
    model = Image
    context_object_name = 'image_list'
    template_name ='user_images.html'
    paginate_by = 2
    
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('title')
    
    
import openai
from django.conf import settings
import urllib.request
from django.core.files import File
from tempfile import NamedTemporaryFile
from django.core.files.base import ContentFile


openai.api_key = settings.OPENAI_API_KEY
model_engine = "davinci"  # Replace with either "davinci" or "curie" or "image-alpha-001"

@login_required
def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', 'default prompt')
        response = openai.Image.create(
            # engine=model_engine,
            prompt=prompt,
            # max_tokens=2048,
            size='256x256',
            # nft=True,
            # stop=None,
        )
        image_url = response['data'][0]['url']
        user = request.user
        image = Image(user=user)
        image.image_file.save(f"{prompt}.jpg", ContentFile(urllib.request.urlopen(image_url).read()))
        image.save()
        return HttpResponse('Image generated and saved successfully!')
    return render(request, 'generate_image.html')

