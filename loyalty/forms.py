from django import forms
from .validators import validate_file_extension

class file_form(forms.Form):
    file=forms.FileField(help_text='text files ".txt" only', validators=[validate_file_extension])
