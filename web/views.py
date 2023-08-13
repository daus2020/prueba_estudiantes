from django.shortcuts import render
from web.models import *
from web.forms import MainForm


def index(request):
    if request.method == 'POST':
        # aqui debe crearse instancia con los datos que colocó el usuario en el formulario
        # form = MainForm(request.POST)
        region_buscada = request.POST.get('region_selector')
        curso_buscado = request.POST.get('curso_selector')
        print(region_buscada, curso_buscado)

        datos = []
        mensaje = ''

        # students = Estudiante.objects.select_related(
        #     'codigo_curso__codigo_plan_formativo').all()

        # print(students)
        # for estudiante in students:
        #     nombre_estudiante = estudiante.nombre
        #     codigo_curso = estudiante.codigo_curso.codigo_curso
        #     descripcion_plan_formativo = estudiante.codigo_curso.codigo_plan_formativo.descripcion

        #     print(nombre_estudiante)
        #     print(codigo_curso)
        #     print(descripcion_plan_formativo)

        if region_buscada != '':
            datos = Estudiante.objects.filter(codigo_comuna__codigo_region=region_buscada).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                                  'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_buscado != '' and region_buscada == '':
            datos = Estudiante.objects.filter(codigo_curso=curso_buscado).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_buscado != '' and region_buscada != '':
            datos = Estudiante.objects.filter(codigo_comuna__codigo_region=region_buscada, codigo_curso=curso_buscado).values('id_estudiante', 'rut', 'nombre', 'apellido_pat',
                                                                                                                              'apellido_mat', 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if curso_buscado == '' and region_buscada == '':
            datos = Estudiante.objects.filter().values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'codigo_curso',
                                                       'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        if len(datos) == 0:
            mensaje = "No existen estudiantes con el criterio de búsqueda seleccionado"

        context = {'estudiantes': datos, 'form': MainForm(
        ), 'region': region_buscada, 'curso': curso_buscado, 'mensaje': mensaje}

    else:
        # aqui debe crearse instancia vacía del formulario
        form = MainForm()
        datos = []
        context = {'estudiantes': datos, 'form': form}

    return render(request, 'form.html', context)
