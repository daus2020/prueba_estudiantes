from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from web.models import *
from web.forms import MainForm, RegistroUsuarioForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def indexView(request):
    return render(request, 'index.html', {'navbar': 'index'})


# @login_required
# def listarVehiculo(request):
#     vehiculos = VehiculoModel.objects.all()
#     context = {'lista_vehiculos': vehiculos, 'navbar': 'lista'}
#     return render(request, "lista.html", context)


@login_required
def listarView(request):
    if request.method == 'POST':
        # aqui debe crearse instancia con los datos que colocó el usuario en el formulario
        # form = MainForm(request.POST)
        region_selected = request.POST.get('region_selector')
        curso_selected = request.POST.get('curso_selector')
        print(region_selected, curso_selected)

        data = []
        message = ''

        # estudiantes = Estudiante.objects.select_related(
        #     'codigo_comuna__codigo_region').all()

        if region_selected != '' and curso_selected == '':
            # data = estudiantes.filter(codigo_comuna__codigo_region=region_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
            #                                                                                'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')
            data = Estudiante.objects.filter(codigo_comuna__codigo_region=region_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                                  'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        elif curso_selected != '' and region_selected == '':
            data = Estudiante.objects.filter(codigo_curso=curso_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat',
                                                                                 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        elif curso_selected != '' and region_selected != '':
            data = Estudiante.objects.filter(codigo_comuna__codigo_region=region_selected, codigo_curso=curso_selected).values('id_estudiante', 'rut', 'nombre', 'apellido_pat',
                                                                                                                               'apellido_mat', 'codigo_curso', 'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')

        # if curso_selected == '' and region_selected == '':
        else:
            data = Estudiante.objects.filter().values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'codigo_curso',
                                                      'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')
            print('else 55')

        if len(data) == 0:
            message = "No existen órdenes con el criterio de búsqueda seleccionado"

        try:
            region_selected_obj = Region.objects.get(
                codigo_region=int(region_selected))
            region_selected = region_selected_obj.nombre
            print(region_selected)
        except (ValueError, TypeError, Region.DoesNotExist):
            region_selected = 'sin filtro aplicado'

        if curso_selected is not None:
            try:
                curso_selected = int(curso_selected)
                print('69-')
            except (ValueError, TypeError):
                pass
                # curso_selected = None
                # message = 'sin filtro aplicado'
                # print('56-')
        total = len(data)

        context = {
            'estudiantes': data,
            'form': MainForm(),
            'region': region_selected,
            'curso': curso_selected if curso_selected is not None else 'sin filtro aplicado',
            'message': message,
            'total': total,
            # 'message': message if 'message' in locals() else None
        }

        # try:
        # # Assuming curso_selected is the field value
        #     curso_selected = int(curso_selected)  # Convert to int if not empty
        # except (ValueError, TypeError):
        #     curso_selected = None  # Handle cases where it's empty or not an int

        # Now, you can set the value to be sent to the context
        # if curso_selected is not None:
        #     try:
        #         curso_selected_obj = Curso.objects.get(id=curso_selected)
        #         context = {'curso_selected': curso_selected_obj.curso_codigo}
        #     except Curso.DoesNotExist:
        #         context = {'curso_selected': 'sin filtro aplicado'}
        # else:
        #     context = {'curso_selected': 'sin filtro aplicado'}

        # try:
        #     curso_selected_obj = Curso.objects.get(
        #         codigo_curso=curso_selected)
        #     curso_selected = curso_selected_obj.codigo_curso
        # except (ValueError, Curso.DoesNotExist):
        #     curso_selected = 'sin filtro aplicado'

        # context = {'estudiantes': data, 'form': MainForm(
        # ), 'region': region_selected, 'curso': curso_selected, 'message': message}

    else:
        form = MainForm()
        data = Estudiante.objects.filter().values('id_estudiante', 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'codigo_curso',
                                                  'codigo_curso__codigo_plan_formativo__descripcion', 'codigo_comuna__nombre', 'codigo_comuna__codigo_region__nombre')
        total = len(data)
        context = {'estudiantes': data, 'form': form, 'total': total}
        # aqui debe crearse instancia vacía del formulario
        # form = MainForm()
        # data = []
        # context = {'estudiantes': data, 'form': form}
        print('ELSE 125')

    print(context)

    return render(request, 'form.html', context)


def registroView(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():

            user = form.save()

            # user.user_permissions.add(visualizar_catalogo)

            login(request, user)
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('listar')
        messages.error(request, 'Registro inválido. Verifique')

    form = RegistroUsuarioForm()
    context = {"register_form": form}
    return render(request, 'registro.html', context)


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Iniciaste sesión como: {username}.")
                return redirect('listar')
            else:
                messages.error(request, "Usuario y/o password inválido(s)")

    form = AuthenticationForm()
    context = {"login_form": form}
    return render(request, "login.html", context)
    # user = authenticate(username, password)


#


def logoutView(request):
    logout(request)
    messages.info(request, "Sesión cerrada exitosamente.")
    return HttpResponseRedirect('/')


def detalleView(request, pk):
    details = Estudiante.objects.filter(rut=pk).values(
        'rut', 'nombre', 'apellido_pat', 'apellido_mat')
    # 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'curso__codigo_plan_formativo__descripcion')
    # 'rut', 'nombre', 'apellido_pat', 'apellido_mat', 'codigo_curso__codigo_plan_formativo__descripcion')
    print('details: ')
    print(details[0])
    print('------------')

    return render(request, 'detalle.html', {'estudiante': details[0], 'id': pk})
