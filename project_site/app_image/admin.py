from django.contrib import admin
from django.utils.html import format_html
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ('title', 'description')
    search_fields = ('title', 'description')
    list_display = ('title', 'description', 'image_thumbnail')
    def image_thumbnail(self, obj):
        return format_html(f'<img src="{obj.image_file.url}" width="100" height="100" />')
    image_thumbnail.short_description = 'Thumbnail'

