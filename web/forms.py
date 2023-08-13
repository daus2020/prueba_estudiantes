from django import forms
from web.models import *

#sex = (('','Seleccione Género'),('F','F'),('M','M'))

class MainForm(forms.Form):
    region_selector = forms.ModelChoiceField(queryset=Region.objects.all().order_by('nombre'), to_field_name='codigo_region', label= "Región", widget=forms.Select(attrs={'class':'form-select'}), required=False, empty_label="Elija una región")
    curso_selector = forms.ModelChoiceField(queryset=Curso.objects.all().order_by('codigo_curso'), to_field_name='codigo_curso', label="Curso", widget=forms.Select(attrs={'class':'form-select'}), required=False, empty_label="Elija un curso")
#    genero = forms.ChoiceField(choices = sex, label="Gender", widget=forms.Select(attrs={'class':'form-select'}), required=False)