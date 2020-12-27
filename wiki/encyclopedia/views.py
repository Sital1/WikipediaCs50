from django.shortcuts import render,redirect
from markdown2 import Markdown
from . import util
from django import forms
from django.contrib import messages
import random




class NewForm(forms.Form):
    title = forms.CharField(label='Title',max_length=50)
    textarea= forms.CharField(widget=forms.Textarea,label='')
    edit = forms.BooleanField(initial="False",widget=forms.HiddenInput,required=False)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request,name):
    markdowner = Markdown()
    html = util.get_entry(name)
    if(html!=None):
        return render(request,"encyclopedia/entry.html",{
            "title":name,
            "content":markdowner.convert(html)
        })


    return render(request,"encyclopedia/entry.html",{
        "title":name,
        "content":f"{name} !!! No such entry"
    })

def search(request):
    value = request.GET.get('q','')
    query = []
    if(util.get_entry(value)!= None):
        query.append(value)
        return render(request, "encyclopedia/index.html", {
        "entries": query,
        "search":True,
        "value":value
        })
    pages = util.list_entries()
    for p in pages:
        if(value.upper() in p.upper()):
            query.append(p)
    return render(request, "encyclopedia/index.html", {
        "entries": query,
        "search":True,
        "value":value
        })

def newpage(request):
    if request.method == 'POST':
        form = NewForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            edit = form.cleaned_data["edit"]

            if title in entries and edit == False:
                messages.warning(request, f'{title} already exixts')
            else:
                util.save_entry(title,textarea)
                markdowner = Markdown()
                html = util.get_entry(title)
                if(html!=None):
                    return render(request,"encyclopedia/entry.html",{
                        "title":title,
                        "content":markdowner.convert(html)
                    })
            
    else:
            form = NewForm()
        
    return render(request,'encyclopedia/newpage.html',{
        "form":form
    })

def edit(request,name):
  
    form = NewForm()
    form.fields["title"].initial = name
    form.fields["title"].disabled = True
    form.fields["textarea"].initial = util.get_entry(name)
    form.fields["edit"].initial = True
    return render(request,'encyclopedia/editpage.html',{
        "form":form
    })

def randomPage(request):
    pages = random.choice(util.list_entries())
    return redirect(entry,name=pages)