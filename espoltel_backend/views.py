from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from flask import Flask, render_template, request


def saludo(request):
    return HttpResponse("Hola, mundo!")

def numero(request, num):
    if num >= 10:
        return HttpResponse("Número: " + str(num))
    else:
        return HttpResponse("Número menor a 10")

def vista(request):
    return render(request,"vista.html",{})

def dinamico(request, username):

    categories = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'num10']

    contexto = {'name': username,
                'categorias': categories}
     
    return render(request,"dinamico.html",contexto)

def estaticos(request):
    return render(request,"estaticos.html",{})

def herencia(request):
    return render(request,"herencia.html",{})

def hijo1(request):
    return render(request,"hijo1.html",{})
def hijo2(request):
    return render(request,"hijo2.html",{})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        return render(request,"dinamico.html",{'name': username})
    else:
        return render(request,"form.html",{})

