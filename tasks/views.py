from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # Formuladrio de creacion y comprobacion de usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate  # crea la cookies
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# ** cuando una url sea visitada


def home(request):  # Renderiza lo que se encuentre en la funcion
    return render(request, "home.html")

# registrar un nuevo user
@login_required
def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # Creacion de usuarios
            try:
                user = User.objects.create_user(
                    username=request.POST[
                        "username"
                    ],  # se compara los label pass1 y pass2
                    password=request.POST["password1"],
                )
                user.save()  # se guarda el registro
                # aqui se genera la Cookie para el inicio de sesion
                login(request, user)
                return redirect("tasks")
            except IntegrityError:  # se captura el error de usuario unico con integrityerror
                return render(
                    request,
                    "signup.html",
                    {  # ! esta alerta o error se muestra en el mismo formulario
                        "form": UserCreationForm,  # se llama al mismo formulario para mostrar el error
                        "error": "Username realy exits",  # las comillas son importantes
                    },
                )
        return render(
            request,
            "signup.html",
            {
                "form": UserCreationForm,  # se envia llama al mismo formulario para mostrar el error
                "error": "Password do not match",
            },
        )


# Mostrar tareas del user no completadas
@login_required # decorador para proteger la rota, no cualquier persona puede entrar a ella
def tasks(request):

    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=True)  # aqui trae las tareas del usuario logeado, muestra tareas no completadas
    print(tasks)
    return render(request, "tasks.html", {"tasks": tasks})  # la variable 'tasks' trae lo q este en el modelo


# Mostrar tareas completdas
@login_required
def tasks_complete(request):

    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  # aqui trae las tareas del usuario logeado, muestra tareas no completadas
    return render(request, "tasks.html", {"tasks": tasks})

# mostrar tarea por separado
@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(
            Task, pk=task_id, user=request.user
        )  # muestra la tarea q les correspone como user
        form = TaskForm(
            instance=task
        )  # crea una instancia del contenido del formulario
        return render(
            request, "task_detail.html", {"task": task, "form": form}
        )  # variabled 'task_detail' 'form'
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()  # guarda y actuliza el formulario de la tarea
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": form, "error": "Error updating task"},
            )

# funcion q mo completa las tareas pendientes
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

# Eliminar tarea
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

# Crear Tareas
@login_required
def create_task(request):

    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")

        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Please provide valida data"},
            )


# aqui cerramos la sesion iniciada con una libreria llamada logout
@login_required
def signout(request):
    logout(request)
    return redirect("home")


# Logeo para iniciar sesion

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")
