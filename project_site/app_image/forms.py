from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'image_file')


class GeneratedImageForm(forms.ModelForm):
    # user = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Image
        fields = ['title', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Enter your prompt here'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GeneratedImageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user.id
