from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms
import markdown2

class new_entry_form(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class":"entry-title", "placeholder":"Enter your page title here..."}),
            label=""
        )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class":"entry-content", "placeholder":"Enter your page content here..."}),
            label=""
        )

def index(request):
    search = request.GET.get('q')
    form = forms.Form(search)
    #if search term is submitted, check if search term is substring of any entry, else displays list of all entries
    if form.is_valid():
        entries = []
        for entry in util.list_entries():
            if search.lower() == entry.lower():
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"name": entry}))
            elif search.lower() in entry.lower():
                entries.append(entry)

        title = "Search results for '" + search + "'"
    else:
        title = 'All Pages'
        entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "title": title,
    })

def entry_page(request, name): #gets and displays content for an entry
    content = util.get_entry(name)

    if content == None:
        content = "No such entry found"
        name = 'ERROR'

    content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title":name,
        "content":content
    })

def new_page(request): #creates a new entry if form data is valid
    if request.method == "POST":
        form = new_entry_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            #checks if entry title conflicts with any existing ones
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    form.add_error("title", "Entry title already exists! Please try another name.")
                    return render(request, "encyclopedia/newpage.html", {
                        "form": form
                    })
            #create the entry since entry title does not conflict with any existing ones
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"name": title}))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": new_entry_form()
        })


def edit_page(request, name):
    if request.method == "POST":
        name = request.POST.get('name')
        content = request.POST.get('content')

        if content!='':
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"name": name}))

    content = util.get_entry(name)
    return render(request, "encyclopedia/editpage.html", {
        "title":name,
        "content":content,
    })

#shuffles list of all entries then goes to the first one in the list
import random
def random_page(request):
    all_entries = util.list_entries()
    random.shuffle(all_entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"name": all_entries[0]}))
