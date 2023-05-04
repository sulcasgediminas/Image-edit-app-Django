from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageForm
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


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