# -*- cpding:utf8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from blog.models import Post, Comment

from .models import UserProfile

from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm


def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.session['login_from'] )
				else:
					return HttpResponse("Disabled account.")
			else:
				return HttpResponse("Invalid login")
	else:
		request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
		form = LoginForm()
	return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    redirect_to = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(redirect_to)


@login_required
def profile(request):
	profile = UserProfile.objects.get(user=request.user)
	posts = Post.objects.filter(author=request.user)
	comments = Comment.objects.filter(name=request.user)
	return render(request, 'accounts/profile.html', 
		                   {'profile': profile,
		                    'posts': posts,
		                    'comments': comments})


@login_required
def edit(request):
	if request.method == "POST":
		user_form = UserForm(instance=request.user, data=request.POST)
		profile_form = ProfileForm(instance=request.user.profile, 
			                       data=request.POST, 
			                       files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, '成功啦')
		else:
			messages.error(request, '失败了')
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'accounts/edit.html', {'user_form': user_form,  'profile_form': profile_form})



def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			
			u = UserProfile(user=new_user)
			u.save()

			login(request, new_user)
			return HttpResponseRedirect(reverse('accounts:profile'))
	else:
		form = RegistrationForm()
	return render(request, 'accounts/register.html', {'form': form})


# github

import urllib


GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_CLIENTID = '9890f2416a5ee83e8da8'
GITHUB_CLIENTSECRET = '9ad5f139646112dd848a295b1b708730fe4152f2'
GITHUB_CALLBACK = 'http://127.0.0.1:8000/accounts/github/'


def _get_refer_url(request):
	refer_url = request.META.get('HTTP_REFER', '/')
	host = request.META['HTTP_HOST']
	if refer_url.startswith('http') and host not in refer_url:
		refer_url = '/'
	return refer_url


# 第一步: 请求github第三方登录
def githhub_login(request):
	data = {
	    'client_id': GITHUB_CLIENTID,
	    'client_secret': GITHUB_CLIENTSECRET,
	    'redirect_uri': GITHUB_CALLBACK,
	    'state': _get_refer_url(request),
	}

	github_auth_url = '{}?{}'.format(GITHUB_AUTHORIZE_URL,urllib.parse.urlencode(data))
	
	print('git_hub_auth_url',github_auth_url)
	return HttpResponseRedirect(github_auth_url)


def github_auth(request):
	template_html = 'accounts/login.html'

	# 如果申请登陆页面成功后，就会返回code和state(被坑了好久)
	if 'code' not in request.GET:
		return render(request,template_html)

	code = request.GET.get('code')

	# 第二步
	# 将得到的code，通过下面的url请求得到access_token

	url = 'https://github.com/login/oauth/access_token'
	data = {
	    'grant_type': 'authorization_code',
	    'client_id': GITHUB_CLIENTID,
	    'client_secret': GITHUB_CLIENTSECRET,
	    'code': code,
	    'redirect_uri': GITHUB_CALLBACK,
	}

	data = urllib.parse.urlencode(data)

	# 请求参数需要bytes类型

	binary_data = data.encode('utf8')
	print('data:', data)

	# 设置请求返回的数据类型
	headers={'Accept': 'application/json'}
	req = urllib.request.Request(url, binary_data,headers)
	print('req:', req)
	response = urllib.request.urlopen(req) 

	# json是str类型的，将bytes转成str
	result = result.decode('ascii')
	result = json.loads(result)
	access_token = result['access_token']
	# print('access_token:', access_token)

	url = 'https://api.github.com/user?access_token={}'.format(access_token)

	response = urllib.request.urlopen(url)
	html = response.read()
	html = html.decode('ascii')
	data = json.loads(html)
	username = data['name']

	# print('username:', username)
	password = '111111'

	# 如果不存在username，则创建
	try:
		user1 = User.objects.get(username=username)
	except:
		user2 = User.objects.create_user(username=username, password=password)
		user2.save()
		profile = Profile.objects.create(user=user2)
		profile.save()

	# 登陆认证
	user = authenticate(username=username, password=password)
	login(request, user)
	return HttpResponseRedirect(reverse('home:index'))