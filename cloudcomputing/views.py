from django.shortcuts import render

# Create your views here.
def user_mode(request):
    return render(request, 'cloudcomputing/user_mode.html',{})

def guest_mode(request):
    return render(request, 'cloudcomputing/guest_mode.html',{})

def user_set(request):
    return render(request, 'cloudcomputing/user_set.html',{})

def change_pw(request):
    return render(request, 'cloudcomputing/change_pw.html',{})

def main(request):
    return render(request, 'cloudcomputing/main.html',{})
def help(request):
    return render(request, 'cloudcomputing/help.html',{})
def login(request):
    return render(request, 'cloudcomputing/login.html',{})
def trash(request):
    return render(request, 'cloudcomputing/trash.html',{})

def create(request):
    return render(request, 'cloudcomputing/create.html',{})