from django.shortcuts import redirect


def index(request):
    return redirect('Restorations:cards', permanent=True)