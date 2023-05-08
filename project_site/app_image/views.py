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

from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages



def index(request):
    num_images = Image.objects.all().count()
    context = {
        'num_images': num_images,
    }
    return render(request, 'index.html', context=context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


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
        words = prompt.split(",")[:1]
        title = ' '.join(words)
        description = f"{prompt}"
        image = Image(user=user, title=title, description=description)
        image.image_file.save(f"{prompt}.jpg", ContentFile(urllib.request.urlopen(image_url).read()))
        image.save()
        return HttpResponse('Image generated and saved successfully!')
    return render(request, 'generate_image.html')

