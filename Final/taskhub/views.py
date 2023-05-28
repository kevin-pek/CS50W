from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import *
from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("noticeboard"))
    else:
        return HttpResponseRedirect(reverse("login"))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["content", "start", "deadline"]
        widgets = {
            "start" : forms.DateTimeInput(attrs={'type':'date'}),
            "deadline" : forms.DateTimeInput(attrs={'type':'date', 'class': 'timepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'required': ''})
        self.fields['deadline'].widget.attrs.update({'required': ''})

def create_task(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            #CREATION OF TASK AND SUBTASKS
            subtask_formset = formset_factory(TaskForm, extra=1, can_order=True, can_delete=True)
            formset = subtask_formset(request.POST)
            data = formset.cleaned_data
            content = data[0].get("content")
            start = data[0].get("start")
            deadline = data[0].get("deadline")

            task = Task.objects.create(content=content, start=start, deadline=deadline, user=request.user)
            task.save()

            #create subtasks and append to main task
            for i in range(formset.total_form_count() - 1):
                content = data[i+1].get("content")
                start = data[i+1].get("start")
                deadline = data[i+1].get("deadline")

                subtask = Task.objects.create(content=content, start=start, deadline=deadline, parent_task=task)
                subtask.save()

        return HttpResponseRedirect(reverse("changeview", kwargs={"viewname": request.user.current_view}))
    else:
        return render(request, "taskhub/login.html")

def toggle_task(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            #TO TOGGLE COMPLETION OF A TASK
            task_id = request.POST["task_id"]
            task = Task.objects.get(pk=task_id)

            if task.parent_task == None:
                task.is_completed = not task.is_completed
                task.save()

                #TOGGLING A PARENT TASK CHANGES COMPLETION OF ALL SUBTASKS TO SAME AS PARENT
                for subtask in Task.objects.filter(parent_task=task):
                    subtask.is_completed = task.is_completed
                    subtask.save()
            else:
                #IF PARENT TASK COMPLETED, CANNOT TOGGLE SUBTASK TO NOT COMPLETED
                if not task.parent_task.is_completed:
                    task.is_completed = not task.is_completed
                    task.save()

            #body_unicode = request.body.decode('utf-8')
            #data = json.loads(body_unicode)

        return HttpResponseRedirect(reverse("changeview", kwargs={"viewname": request.user.current_view}))
    else:
        return HttpResponseRedirect(reverse("login"))


def delete_task(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            task_id = request.POST["task_id"]
            task = Task.objects.get(pk=task_id)
            task.delete()

        return HttpResponseRedirect(reverse("changeview", kwargs={"viewname": request.user.current_view}))
    else:
        return HttpResponseRedirect(reverse("login"))

def changeview(request, viewname):
    if request.user.is_authenticated:
        subtask_formset = formset_factory(TaskForm, extra=1, can_order=True, can_delete=True)

        #UPDATE USER'S VIEW
        request.user.current_view = viewname

        #FILTER TO EXCLUDE SUBTASKS
        if viewname == "All":
            tasks = Task.objects.filter(parent_task=None)
        elif viewname == "Completed":
            tasks = Task.objects.filter(is_completed=True, parent_task=None)
        elif viewname == "Incomplete":
            tasks = Task.objects.filter(is_completed=False, parent_task=None)

        return render(request, "taskhub/tasks.html", {
            "tasks": tasks,
            "formset": subtask_formset
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def noticeboard(request):
    if request.user.is_authenticated:
        return render(request, "taskhub/noticeboard.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def load_board(request, boardname):
    if request.user.is_authenticated:
        #RETURNS NOTES IN USER'S CURRENT BOARD IN JSON FORMAT
        board = Board.objects.get(title=request.user.username)
        notes = board.notes.all()

        return JsonResponse([note.serialise() for note in notes], safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))

def create_board(request, boardname = "default"):
    if request.user.is_authenticated:
        board.objects.create(title=request.user.username)

        return HttpResponseRedirect(reverse("noticeboard"))
    else:
        return HttpResponseRedirect(reverse("login"))

def add_note(request, boardname):
    if request.user.is_authenticated:
        #CREATE A NEW NOTEFOR CURRENT BOARD IN VIEW
        board = Board.objects.get(title=request.user.username)
        note = Note.objects.create(board=board)
        note.save()

        return JsonResponse(note.serialise(), safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def update_note(request, note_id):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid Data."})

        note = Note.objects.get(pk=note_id)
        note.content = data.get("content")
        note.x_coord = data.get("x_coord")
        note.y_coord = data.get("y_coord")
        note.width = data.get("width")
        note.height = data.get("height")
        note.save()

        return JsonResponse({"message": "Saved successfully."}, status=201)
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def delete_note(request, note_id):
    if request.user.is_authenticated:
        note = Note.objects.get(pk=note_id)
        note.delete()

        return HttpResponseRedirect(reverse("noticeboard"))
    else:
        return HttpResponseRedirect(reverse("login"))

def calendar(request):
    if request.user.is_authenticated:
        return render(request, "taskhub/calendar.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def get_tasks(request):
    if request.user.is_authenticated:
        #RETURNS USER'S TASKS IN JSON FORMAT
        tasks = Task.objects.filter(user=request.user, is_completed=False)
        return JsonResponse([task.serialise() for task in tasks], safe=False)
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "taskhub/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "taskhub/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "taskhub/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except:
            return render(request, "taskhub/register.html", {
                "message": "Username already taken."
            })
        board = Board.objects.create(title=user.username)
        board.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "taskhub/register.html")
