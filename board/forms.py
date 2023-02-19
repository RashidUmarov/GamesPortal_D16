from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Response


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
            'attach',
        ]
        labels = {'title': ('Заголовок'),
                  'content': (''),
                  'category': ('Категория'),
                  'attach': ('Вложение'),
                  }
        """
        widgets = {'attach': forms.FileInput(
                attrs={'class': 'form-control'},
            ),
        }
        """

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)
        labels = {'text': (''),
                  }
