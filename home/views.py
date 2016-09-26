from django.shortcuts import render


def index(request):
	a = request.META.get('HTTP_REFERER', '/')
	return render(request, 'home/index.html', {'a': a})