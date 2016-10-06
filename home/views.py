import json
from django.shortcuts import render


def index(request):
    l = 'woca'
    return render(request, 'home/index.html', {'l': json.dumps(l)})