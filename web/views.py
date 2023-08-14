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
            'codigo_comuna__codigo_region').all()
        # estudiantes = Estudiante.objects.select_related(
        #     'codigo_curso__codigo_plan_formativo').all()

        # print(estudiantes)
        # for estudiante in estudiantes:
        #     nombre_estudiante = estudiante.nombre
        # codigo_curso = estudiante.codigo_curso.codigo_curso
        # codigo_curso = estudiante.codigo_curso
        # descripcion_plan_formativo = estudiante.codigo_curso.codigo_plan_formativo.descripcion

        # for item in estudiantes:
        #     print(item.nombre)
        #     print(item.codigo_curso.codigo_curso)
        #     # print(item.codigo_curso.codigo_curso.codigo_curso)
        #     print(item.codigo_curso.codigo_plan_formativo.descripcion)
        # print(nombre_estudiante)
        # print(codigo_curso)
        # print(descripcion_plan_formativo)

        if region_selected != '':
            data = estudiantes.filter(codigo_comuna__codigo_region=region_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                           'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')
            # data = Estudiante.objects.filter(codigo_comuna__codigo_region=region_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
            #                                                                                       'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

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

        # try:
        #     region_selected = Region.objects.get(
        #         codigo_region=int(region_selected.nombre))
        # except Region.DoesNotExist:
        #     # Handle the case where the specified region does not exist
        #     region_selected = 'sin filtro aplicado'
        # pass
        # try:
        #     region_selected = Region.objects.get(
        #         codigo_region=int(region_selected))
        # except Region.DoesNotExist:
        #     region_selected = None
        # try:
        #     region_selected = Region.objects.get(
        #         codigo_region=[int(region_selected) - 1].nombre)
        # except Region.DoesNotExist:
        #     region_selected = 'sin filtro aplicado'

        # try:
        #     region_selected = Region.objects.get(
        #         codigo_region=int(region_selected))
        #     region_nombre = region_selected.nombre
        # except Region.DoesNotExist:
            # Handle the case where the specified region does not exist
            # region_nombre = 'sin filtro aplicado'

        # if region_selected:
        #     region_selected = Region.objects.all(
        #     )[int(region_selected) - 1].nombre
        #     # region_selected = Region.objects.all(
        #     # )[int(region_selected) - 1].nombre
        # else:
        #     region_selected = 'sin filtro aplicado'
        # # region_selected = Region.objects.filter(
        # #     codigo_region=region_selected).values('nombre')[0]
        # # codigo_region=region_selected.values('nombre')
        # print(region_selected)

        try:
            region_selected_obj = Region.objects.get(
                codigo_region=int(region_selected))
            region_selected = region_selected_obj.nombre
        except (ValueError, Region.DoesNotExist):
            region_selected = 'sin filtro aplicado'

        context = {'estudiantes': data, 'form': MainForm(
        ), 'region': region_selected, 'curso': curso_selected, 'message': message}

    else:
        # aqui debe crearse instancia vacía del formulario
        form = MainForm()
        data = []
        context = {'estudiantes': data, 'form': form}

    return render(request, 'form.html', context)
