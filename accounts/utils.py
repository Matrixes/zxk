# 获取用户登录前的url或者next参数的，写进session，提升用户体验
# 主要为了login_required

def redirect_to(request):
	login_from = request.META.get('HTTP_REFERER', '/')

	# 优先获取带next的url
	next= request.GET.get('next')
	if next:
		protocol = "https" if request.is_secure() else "http"
		host = request.get_host()
		login_to = protocol + "://" + host + next
		return login_to

	return login_from