# -*- cpding:utf8 -*-


import re
import json
import random
import string
import requests

from pprint import pprint
from requests_oauthlib import OAuth2Session

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse  以前的地点
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from blog.models import Post, Comment

from .models import UserProfile, UserSettings, SocialUser, Contack, Collections

from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, \
                   PasswordChangeForm, UserSettingsForm

from .utils import  redirect_to

from actions.utils import create_action
# Display activity stream
from actions.models import Action
from images.models import Image

# ajax_login

#@require_POST
#def ajax_login(request):
#	username = request.POST.get('username').strip()
#	password = request.POST.get('password')
#
#	if User.objects.filter(username=username):
#		user = authenticate(username=username, password=password)
#		if user:
#			if user.is_active:
#				login(request, user)
#				print(username, password)
#				return render(request, 'blog/index.html')
#		else:
#			return HttpResponse("user error")
#	else:
#		return HttpResponse("username not found")



def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.session['to'])
				else:
					messages.warning(request, 'user is not active.')
			else:
				messages.error(request, 'username/passwird is wrong')
		else:
			messages.error(request, form.errors)

		# avoid refresh post
		return redirect(reverse('accounts:login'))
	else:
		request.session['to'] = redirect_to(request)
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
	# posts = Post.objects.filter(author=request.user)
	# comments = Comment.objects.filter(name=request.user)
	return render(request, 'accounts/admin/profile.html',  {'profile': profile}) #, 'posts': posts, 'comments': comments})


# 这个不用了，见下面的yser_detail
def user(request, id):
	user = get_object_or_404(User, id=int(id))
	
	if request.user == user:
		return redirect(reverse('accounts:profile'))

	posts = Post.objects.filter(author=user)
	comments = Comment.objects.filter(name=user)
	return render(request, "accounts/user.html", {'user': user, 'posts': posts, 'comments': comments})



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

			create_action(request.user, '修改了', request.user.profile)

			messages.success(request, '成功啦')
		else:
			messages.error(request, user_form.errors)

		return redirect(reverse('accounts:edit'))
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'accounts/admin/edit.html', {'user_form': user_form,  'profile_form': profile_form})

@login_required
def password_change(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = request.user.username
			user = authenticate(username=username, password=cd['old_password'])
			if user:
				user.set_password(cd['new_password'])
				user.save()
				messages.success(request, '成功啦')
			else:
				messages.error(request, '密码错误')
	else:
		form = PasswordChangeForm()
	return render(request, 'accounts/admin/password-change.html', {'form': form})

# 账户关联信息
#############以后再搞#########


# 用户设置信息

## 紧急通知，由于写成了instance=request.user，至少在这上面浪费了4个小时
## 应该为instance=request.user.settings，看来还是理解不够深刻
@login_required
def user_settings(request):
	if request.method == 'POST':
		form = UserSettingsForm(instance=request.user.settings, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "设置成功")
		else:
			messages.error(request, form.errors)
		return redirect(reverse('accounts:user_settings'))
	else:
		form = UserSettingsForm(instance=request.user.settings)
	return render(request, 'accounts/admin/settings.html', {'form': form})



# 用户注册后记得添加设置等

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			
			# 创建个人资料
			UserProfile.objects.create(user=new_user)
			# 添加设置
			UserSettings.objects.create(user=new_user)
			
			login(request, new_user)

			return HttpResponseRedirect(reverse('accounts:profile'))
	else:
		form = RegistrationForm()
	return render(request, 'accounts/register.html', {'form': form})



# Social Auth

# github

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
authorization_base_url = settings.AUTHORIZATION_BASE_URL
token_url = settings.TOKEN_URL
redirect_uri = settings.RECIRECT_URI
scope = settings.SCOPE

def github_login(request):
	github = OAuth2Session(client_id=client_id, scope=scope)

	# Redirect user to GitHub for authorization
	authorization_url, state = github.authorization_url(authorization_base_url)

	request.session['oauth_state'] = state

	print(request.session['to'])

	return HttpResponseRedirect(authorization_url)


def github_auth(request):
	code = request.GET.get('code')

	github = OAuth2Session(client_id, state=request.session['oauth_state'])

	# 下面的code=code这一项卡住很久
	token = github.fetch_token(token_url, code=code, client_secret=client_secret)
	response = github.get('https://api.github.com/user')

	c1 = response.content  # bytes
	# c2 = response.content()   # Error 'bytes' object is not callable

	t1 = response.text  # str
	# t2 = response.text()  # Error 'str' object is not callable

	j1 = response.json  # method
	res = response.json()  # dict

	pprint(res)

	log_in = res.get('login')  # login is already existed
	email = res.get('email') or ''  # if email is protected, then 'email': None
	github_id = res.get('id')
	avatar_url = res.get('avatar_url')

	s = SocialUser.objects.filter(login=log_in, social_id=github_id)

	if len(s) > 1:
		# raise 404
		pass

	# if u is <QuerySet []>: a is None:False, bool(u): False
	if s:  
		user = User.objects.get(social_user=s[0])
		# user = s[0].user
		if user.is_active:
			login(request, user) # many times str is not callable because login..shit
			return  HttpResponseRedirect(request.session['to'])
		else:
			return HttpResponse("The account is diabled")

	# create new acount

	username = log_in + "_github"
	password = 'git' + ''.join([random.choice(string.printable[:62]) for i in range(5)])
	
	new_user = User(username=username, email=email)
	new_user.set_password(password)
	new_user.save()

	UserProfile.objects.create(user=new_user, nickname=log_in) # photo怎么办
	SocialUser.objects.create(user=new_user, login=log_in, social_id=github_id, belong='GH')
	UserSettings.objects.create(user=new_user)

	# Get photo
	r = requests.get(avatar_url, stream=True)

	print('r.status: ', r.status_code)

	if r.status_code == 200:
		photo_name = settings.MEDIA_ROOT + '/avatar/' + str(github_id)
		with open(photo_name, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				f.write(chunk)
		photo = 'avatar/' + str(github_id)
		new_user.profile.photo = photo
		new_user.profile.save()

	if email:
		subject = "You have created a new account of zuixinke"
		message = "username: {}, password: {}. or use your github to login".format(username, password)
		send_mail(subject, message, 'me@zuixinke.xyz', [email])

	login(request, new_user)

	# return  HttpResponseRedirect(reverse('accounts:profile'))
	return  HttpResponseRedirect(request.session['to'])


#############################


#####################################
# 准备用来显示用户及其关注的人的动态
@login_required
def myhome(request):
	user = request.user

	# Display all actions by default
	actions = Action.objects.all()

	# 提取用户的动态内容 
	return render(request, 'accounts/home/home.html', {'user': user, 'actions': actions})


@login_required
def myposts(request):
	user = request.user
	posts = user.blog_posts.order_by('-publish')
	return render(request, 'accounts/home/posts.html', {'user': user, 'posts': posts})

@login_required
def mycomments(request):
	user = request.user
	comments = user.comments.order_by('-created')
	return render(request, 'accounts/home/comments.html', {'user': user, 'comments': comments})


@login_required
def myshare(request):
	user = request.user
	images = user.images_created.all()
	return render(request, 'accounts/home/share.html', {'user': user, 'images': images})

@login_required
def mydrafts(request):
	user = request.user
	drafts = user.blog_posts.filter(status='D')
	return render(request, 'accounts/home/drafts.html', {'user': user, 'drafts': drafts})

@login_required
def mycollects(request):
	user = request.user
	collects = user.collections.post.all()
	return render(request, 'accounts/home/collects.html', {'user': user, 'collects': collects})


# 关注系统
@login_required
def user_list(request):
	users = User.objects.filter(is_active=True).order_by('username')
	return render(request, 'accounts/user-list.html', {'users': users})


# 查看其它用户的各种信息
def user_home(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	if request.user == user:
		return redirect(reverse('accounts:myhome'))
	actions = Action.objects.all()
	return render(request, 'accounts/other/home.html', {'user': user, 'actions': actions})

def user_posts(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	if request.user == user:
		return redirect(reverse('accounts:myposts'))
	posts = user.blog_posts.order_by('-publish')
	return render(request, 'accounts/other/posts.html', {'user': user, 'posts': posts})

def user_comments(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	if request.user == user:
		return redirect(reverse('accounts:mycomments'))
	comments = user.comments.order_by('-created')
	return render(request, 'accounts/other/comments.html', {'user': user, 'comments': comments})

def user_share(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	if request.user == user:
		return redirect(reverse('accounts:myshare'))
	images = user.images_created.all()
	return render(request, 'accounts/other/share.html', {'user': user, 'images': images})

# 为一个对象设置URL，有两个方法
# 1、在models中定义get_absolute_url()方法
# 2、在settings中添加ABSO;UTE_URL_OVERRIDES

# ABSOLUTE_URL_OVERRIDES = {
#     'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
# }


# AJAX view to follow users

from common.decorators import ajax_required
@ajax_required
@require_POST
@login_required
def user_follow(request):
	user_id = request.POST.get('id')
	action = request.POST.get('action')
	if user_id and action:
		try:
			user = User.objects.get(id=user_id)
			if action == 'follow':
				Contack.objects.get_or_create(user_from=request.user, user_to=user)
				create_action(request.user, '关注了', user)
				
			else:
				Contack.objects.filter(user_from=request.user, user_to=user).delete()
				create_action(request.user, '取消关注', user)

			return JsonResponse({'status': 'ok'})
		except User.DoesNotExist:
			return JsonResponse({'status': 'ko'})
	return JsonResponse({'status': 'ko'})

# 关注列表
def user_following(request, username):
	user = User.get_object_or_404(User, username=str(username))
	follwing_list = user.following.all()
	return render(request, 'accounts/following.html', {'follwing_list', follwing_list})

# 粉丝列表


# 添加到收藏
@ajax_required
@require_POST
@login_required
def collecting(request):
	post_id = int(request.POST.get('id'))
	action = request.POST.get('action')
	if post_id and action:
		try:
			post = Post.objects.get(id=post_id)
			if action == 'collect':
				new_item, status = Collections.objects.get_or_create(user=request.user)
				new_item.post.add(post)
				create_action(request.user, '收藏了', post)
			else:
				Collections.objects.filter(user=request.user, post=post).delete()
				create_action(request.user, '取消收藏', post)

			return JsonResponse({'status': 'ok'})
		except:
			return JsonResponse({'status': 'ko'})
	return JsonResponse({'status': 'ko'})