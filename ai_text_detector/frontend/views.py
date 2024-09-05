from django.shortcuts import render

def index(request):
    return render(request, 'frontend/index.html')


def home(request):
    return render(request, 'index.html')

# ... rest of your views ...