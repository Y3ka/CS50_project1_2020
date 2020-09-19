from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

from . import util
import markdown2
from random import randint


def index(request):
    #user uses the search bar
    if request.method == "POST":
        page_name = request.POST["q"]
        if util.get_entry(page_name) != None:
            html = markdown2.markdown(util.get_entry(page_name))       
            return render(request, "encyclopedia/entry.html", {
                "page_name": page_name,
                "html": html
            })
        else:
            matching_list = [] 
            for entry in util.list_entries():
                if page_name.lower() in entry.lower():
                    matching_list.append(entry)
            if matching_list == []:
                return render(request, "encyclopedia/error.html", {
                    "page_name": page_name
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "list": matching_list,
                    "page_name": page_name
                })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, page_name):
    """ Displays the entry when the user search for the url wiki/page_name.
    It shows an error page when the name does not exist"""

    md_page = util.get_entry(page_name)
    if md_page == None:
        return render(request, "encyclopedia/error.html", {
            "page_name": page_name
        })
    else:
        html = markdown2.markdown(md_page)       
        return render(request, "encyclopedia/entry.html", {
            "page_name": page_name,
            "html": html
        })

def add(request):
    """Create a new entry"""
    if request.method == "POST":
        title_entry = request.POST["title_entry"]
        #check if the entry already exists
        filename = f"entries/{title_entry}.md"
        if default_storage.exists(filename):
            return render(request, "encyclopedia/error_add.html")
        else:
            util.save_entry(title_entry, request.POST["text_entry"])
            md_page = util.get_entry(title_entry)
            html = markdown2.markdown(md_page)       
            return render(request, "encyclopedia/entry.html", {
                "page_name": title_entry,
                "html": html
            })
    return render(request, "encyclopedia/add.html")

def edit(request, page_name):
    """Edit a new entry"""
    if request.method == "POST":
        util.save_entry(page_name, request.POST["text_entry"])
        return redirect(entry, page_name=page_name)
    else:
        md_page = util.get_entry(page_name)
        if md_page == None:
            return render(request, "encyclopedia/error.html", {
                "page_name": page_name
            })
        else:   
            return render(request, "encyclopedia/edit.html", {
                "page_name": page_name,
                "content": md_page
            })

def random(request):
    """Redirect on a random entry"""
    list_entries = util.list_entries()
    print(list_entries)
    nb = randint(0, len(list_entries)-1)
    return redirect(entry, page_name=list_entries[nb])
