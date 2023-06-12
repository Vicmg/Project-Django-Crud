from django import forms
from .models import Task

# aqui traemos los atributos de los modelo que quiero ver en mi formulario
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description','important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Escribe tu titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Breve descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto mb-3'}),
        }