import requests
from urllib.parse import urlparse
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
        'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        # Parse the URL path to safely extract the extension
        path = urlparse(url).path
        extension = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.'
            )
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        path = urlparse(image_url).path
        extension = path.rsplit('.', 1)[-1].lower()
        image_name = f'{name}.{extension}'
        # Download image from the given URL with timeout and error handling
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise forms.ValidationError(f'Could not download the image: {e}')
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        if commit:
            image.save()
        return image
    
