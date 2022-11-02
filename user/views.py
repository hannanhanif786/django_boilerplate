from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Task
from .modelform import TaskForm, RegisterForm, ChangePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MyUser


def registerPage(request):
    """This function based is used to check out the signup functionality

    Args:
        request (request): taking data from request and check user already or not and creared if not

    Returns:
        render: render data to template and perform signup functionality
    """
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                form = RegisterForm()
                return redirect("/login")

        context = {"form": form}
    return render(request, "signup.html", context)


def loginPage(request):
    """This function based is used to check out the login functionality

    Args:
        request (HttpRequest obj): take data for user and check the credentials for this user

    Returns:
        render: response for the data if user credentials match then give access or message wrong credentials
    """
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, "username or password not match")
    return render(request, "login.html")


def logoutPage(request):
    """close the session for the authenticated user

    Args:
        request (_type_): _description_

    Returns:
        redirect: for redirection of page
    """
    logout(request)
    return redirect("/login")


@login_required(login_url="login")
def change_password(request):
    """this is used to change the password for authenticated user with old password

    Args:
        request (HttpRequest object): take old password and new password data

    Returns:
        response: for diff conditions give diff respone
    """
    form = ChangePassword()
    if request.method == "POST":
        form = ChangePassword(data=request.POST)
        if form.is_valid():
            old = form.cleaned_data["oldpasssword"]
            new = form.cleaned_data["newpasssword"]
            confirm = form.cleaned_data["confirm_newpasssword"]
            user = authenticate(username=request.user, password=old)
            print(old, " ", "new", new, "confirm", confirm, user)
            if user is not None:
                if new == confirm:
                    update = MyUser.objects.get(email=request.user)
                    update.set_password(new)
                    update.save()
                    messages.info(request, "Password Updated")
                else:
                    messages.info(
                        request, "new password and confirm password not Matched"
                    )
            else:
                messages.info(request, "Wrong Old password")
    else:
        form = ChangePassword()
    context = {"form": form}
    return render(request, "change_password.html", context)


@login_required(login_url="login")
def home(request):
    return render(request, "index.html")


@login_required(login_url="login")
def create(request):
    """this function based view use for create task

    Args:
        request (HttpRequest object): task data

    Returns:
        render: used for rendering data and check request method and perform functionality
    """
    form = TaskForm
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = TaskForm()
    context = {"form": form}
    return render(request, "form.html", context)


@login_required(login_url="login")
def read(request):
    """this is used to read the all task data

    Args:
        request (HttpRequest object):

    Returns:
        render: render template and show all data in response
    """
    task = Task.objects.all()
    context = {"data": task}
    return render(request, "list.html", context)


@login_required(login_url="login")
def update(request, id):
    """this is used to update data for instance task

    Args:
        request (HttpRequest object):

    Returns:
        render: render template and update  data for instance task
    """
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("/read")
    context = {"form": form}
    return render(request, "form.html", context)


@login_required(login_url="login")
def delete(request, id):
    """this is used to delete data for instance task

    Args:
        request (HttpRequest object):

    Returns:
        render: render template and delete  data for instance task
    """
    obj = Task.objects.get(id=id)
    obj.delete()
    return redirect("/read")
