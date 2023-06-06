from django.shortcuts import render

# Create your views here.

def main(request): #main.html 렌더링
    return render(request, 'main.html',{})

def login(request): #login.html 렌더링
    return render(request, 'login.html',{})

def create(request): #create.html 렌더링
    return render(request, 'create.html',{})

def help(request): #help.html 렌더링
    return render(request, 'help.html',{})

def trash(request): #trash.html 렌더링
    return render(request, 'trash.html',{})

