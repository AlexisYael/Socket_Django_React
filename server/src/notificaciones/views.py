from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'notificaciones/index.html',{})

def room(request, numero_usuario):
    return render(request, 'notificaciones/room.html', {
        'numero_usuario': numero_usuario
    })