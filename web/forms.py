from django import forms
from web.models import *

# sex = (('','Seleccione Género'),('F','F'),('M','M'))


class MainForm(forms.Form):
    region_selector = forms.ModelChoiceField(
        queryset=Region.objects.all().order_by('codigo_region'),
        label="Región", widget=forms.Select(attrs={'class': 'form-select'}),
        required=False, empty_label="Elija una región"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region_selector'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return obj.nombre

    curso_selector = forms.ModelChoiceField(queryset=Curso.objects.all().order_by('codigo_curso'), to_field_name='codigo_curso',
                                            label="Curso", widget=forms.Select(attrs={'class': 'form-select'}), required=False, empty_label="Elija un curso")
    # region_selector = forms.ModelChoiceField(queryset=Region.objects.all().order_by('nombre'), to_field_name='codigo_region',
    #                                          label="Región", widget=forms.Select(attrs={'class': 'form-select'}), required=False, empty_label="Elija una región")

    # Create a custom queryset to fetch the name and value fields
    # custom_queryset = Region.objects.all().values_list('codigo_region', 'nombre')

    # Build the choices list from the custom queryset
    # choices = [(codigo_region, nombre)
    #            for codigo_region, nombre in custom_queryset]

    # Create a ModelChoiceField with the custom choices
    # region_selector = forms.ModelChoiceField(
    #     queryset=Region.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     choices=choices,
    # )
    # region_selector = forms.ModelChoiceField(queryset=Region.objects.all().values_list('codigo_region', 'nombre'),
    #                                          widget=forms.Select(
    #     attrs={'class': 'form-control'}),
    # )

    # class CustomModelChoiceField(forms.ModelChoiceField):
    #     def label_from_instance(self, obj):
    #         return obj.nombre

    # class MyForm(forms.Form):
    #     region_selector = CustomModelChoiceField(
    #         queryset=Region.objects.all(),
    #         widget=forms.Select(attrs={'class': 'form-control'}),
    #         to_field_name='codigo_region',  # Use 'value' field as the value
    #     )
#   region_selector = forms.ModelChoiceField(queryset=Region.objects.all().order_by('nombre'), to_field_name='codigo_region',
#                                              label="Región", widget=forms.Select(attrs={'class': 'form-select'}), required=False, empty_label="Elija una región")

#    genero = forms.ChoiceField(choices = sex, label="Gender", widget=forms.Select(attrs={'class':'form-select'}), required=False)
