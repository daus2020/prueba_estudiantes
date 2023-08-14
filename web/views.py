from django.shortcuts import render
from web.models import *
from web.forms import MainForm


def index(request):
    if request.method == 'POST':
        # aqui debe crearse instancia con los datos que colocó el usuario en el formulario
        # form = MainForm(request.POST)
        region_selected = request.POST.get('region_selector')
        curso_selected = request.POST.get('curso_selector')
        print(region_selected, curso_selected)

        data = []
        message = ''

        estudiantes = Estudiante.objects.select_related(
            'codigo_curso__codigo_plan_formativo').all()

        print(estudiantes)
        for item in estudiantes:
            # for estudiante in estudiantes:
            # nombre_estudiante = estudiante.nombre
            # codigo_curso = estudiante.codigo_curso.codigo_curso
            # descripcion_plan_formativo = estudiante.codigo_curso.codigo_plan_formativo.descripcion

            print(item.nombre)
            print(item.codigo_curso.codigo_curso)
            # print(item.codigo_curso.codigo_curso.codigo_curso)
            print(item.codigo_curso.codigo_plan_formativo.descripcion)
            # print(nombre_estudiante)
            # print(codigo_curso)
            # print(descripcion_plan_formativo)

        if region_selected != '':
            data = Estudiante.objects.filter(codigo_comuna__codigo_region=region_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                                  'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_selected != '' and region_selected == '':
            data = Estudiante.objects.filter(codigo_curso=curso_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_selected != '' and region_selected != '':
            data = Estudiante.objects.filter(codigo_comuna__codigo_region=region_selected, codigo_curso=curso_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat',
                                                                                                                               'apellido_mat', 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_selected == '' and region_selected == '':
            data = Estudiante.objects.filter().values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'codigo_curso',
                                                      'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if len(data) == 0:
            message = "No existen estudiantes con el criterio de búsqueda seleccionado"

        # if region_selected.exists():
        #     region_data = region_selected[0]
        #     region_name = region_data['nombre']
        #     print(region_name)

        if region_selected:
            region_selected = Region.objects.all(
            )[int(region_selected) - 1].nombre
        else:
            region_selected = 'sin filtro aplicado'
        # region_selected = Region.objects.filter(
        #     codigo_region=region_selected).values('nombre')[0]
        # codigo_region=region_selected.values('nombre')
        print(region_selected)

        context = {'estudiantes': data, 'form': MainForm(
        ), 'region': region_selected, 'curso': curso_selected, 'message': message}

    else:
        # aqui debe crearse instancia vacía del formulario
        form = MainForm()
        data = []
        context = {'estudiantes': data, 'form': form}

    return render(request, 'form.html', context)
