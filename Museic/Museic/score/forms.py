import base64

from django.core.files.base import ContentFile

from django.forms.widgets import TextInput


class HandwritingPad(TextInput):
    template_name = 'handwriting/handwriting.html'

    class Media:
        css = {
            'all': (
                'handwriting/css/signpad.css',
            ),
        }

        js = (
            'handwriting/js/signpad.js',
        )

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs['hidden'] = ''
        super().__init__(attrs)

    def is_initial(self, value):
        return bool(value and getattr(value, 'url', False))

    def value_from_datadict(self, data, files, name):
        data_url = super().value_from_datadict(data, files, name)
        if not data_url:
            return None  # Let fields raise ValidationError

        image_format, image_string = data_url.split(';base64,')
        ext = image_format.split('/')[-1]
        return ContentFile(base64.b64decode(image_string), name='temp.' + ext)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'is_initial': self.is_initial(value),
        })
        return context

    def format_value(self, value):
        if not self.is_initial(value):
            return None

        b64_image = base64.b64encode(value.file.read()).decode('utf-8')
        ext = value.name.split('.')[-1]
        return f'data:image/{ext};base64,{b64_image}'