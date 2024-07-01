from django.http import HttpResponse
from django.shortcuts import render


def saludo():
    """
    Returns a HttpResponse with the message "Hola, mundo!"
    """
    return HttpResponse("Hola, mundo!")

def numero(num):
    """
    Returns an HttpResponse with a message based on the value of the input number.

    Args:
        num (int): The input number.

    Returns:
        HttpResponse: An HttpResponse object with a message indicating 
        whether the number is greater than or equal to 10.

    """
    if num >= 10:
        return HttpResponse("Número: " + str(num))
    else:
        return HttpResponse("Número menor a 10")

def vista(request):
    """
    This function is a view that renders the 'vista.html' template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - The rendered 'vista.html' template.
    """
    return render(request,"vista.html",{})

def dinamico(request, username):
    """
    This function renders the 'dinamico.html' template with the given username
    and a list of categories.

    Parameters:
    - request: The HTTP request object.
    - username: The username to be displayed in the template.

    Returns:
    - A rendered HTML response.
    """

    categories = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'num10']

    contexto = {'name': username,
                'categorias': categories}  
    return render(request,"dinamico.html",contexto)

def estaticos(request):
    """
    This function is a view for rendering the 'estaticos.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    return render(request,"estaticos.html",{})

def herencia(request):
    """
    This function handles the request for the 'herencia' view.
    It renders the 'herencia.html' template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'herencia.html' template.
    """
    return render(request, "herencia.html", {})

def hijo1(request):
    """
    This function renders the 'hijo1.html' template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML response.
    """
    return render(request, "hijo1.html", {})


def hijo2(request):
    """
    This function renders the 'hijo2.html' template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'hijo2.html' template.
    """
    return render(request, "hijo2.html", {})

def login(request):
    """
    This function handles the login functionality.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the request method is POST, it returns the 'dinamico.html' template 
    with the username passed as a context variable.
    - If the request method is not POST, it returns the 'form.html' template.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        return render(request,"dinamico.html",{'name': username})
    else:
        return render(request,"form.html",{})
