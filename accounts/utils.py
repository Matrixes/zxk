def redirect_to(request):
	login_from = request.META.get('HTTP_REFERER', '/')

	next= request.GET.get('next')
	if next:
		protocol = "https" if request.is_secure() else "http"
		host = request.get_host()
		login_to = protocol + "://" + host + next
		return login_to

	return login_from