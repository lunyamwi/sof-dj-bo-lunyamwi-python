from django import forms
from ckeditor_uploader.widgets import CKEditorWidget,CKEditorUploadingWidget

class ArticleForm(forms.ModelForm):
    content=forms.CharField(widget=CKEditorUploadingWidget())
