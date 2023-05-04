from django.db import models
from django.conf import settings


class Image(models.Model):
    title = models.CharField(
        max_length=100, #The maximum length of the field will be 100 characters.
        blank=False, #The field will be required and cannot be left blank.
        null=False, #The field will not be able to be set to NULL.
        unique=False, #The field will not have to be unique.
        verbose_name=None, #Django will use the field name with underscores replaced by spaces as the verbose name.
        help_text='Enter title', #The field will have an empty help text.
    )
    description = models.TextField()
    image_file = models.ImageField(upload_to='media/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            self.user = user
        super().save(*args, **kwargs)