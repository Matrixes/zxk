# -*- cpding:utf8 -*-


import re
import random
import string
import requests
from pprint import pprint
from requests_oauthlib import OAuth2Session

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse  以前的地点
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from blog.models import Post, Comment

from .models import UserProfile, SocialUser

from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, \
                   PasswordChangeForm


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
				messages.error(request, '失败了')
	else:
		form = PasswordChangeForm()
	return render(request, 'accounts/password_change.html', {'form': form})


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

	login = res.get('login')
	email = res.get('email') or ''  # if email is protected, then 'email': None
	github_id = res.get('id')
	avatar_url = res.get('avatar.url')

	u = SocialUser.objects.filter(login=login, social_id=github_id)

	if len(u) > 1:
		# raise 404
		pass

	# if u is <QuerySet []>: a is None:False, bool(u): False
	if u:  
		user = User.objects.get(social_user=u)
		if user.is_active:
			login(request, user)
			return  HttpResponseRedirect(reverse('accounts:profile'))
		else:
			return HttpResponse("The account is diabled")

	# create new acount

	username = login + "_github"
	password = 'git' + ''.join([random.choice(string.printable[:62]) for i in range(5)])
	
	new_user = User(username=username, email=email)
	new_user.set_password(password)
	new_user.save()

	UserProfile.objects.create(user=new_user, nickname=login) # photo怎么办
	SocialUser.objects.create(user=new_user, login=login, social_id=github_id, belong='GH')

	if email:
		subject = "You have created a new account of zuixinke"
		message = "username: {}, password: {}. or use your github to login".format(username, password)
		send_mail(subject, message, 'me@zuixinke.xyz', [email])

	login(request, new_user)

	# return  HttpResponseRedirect(reverse('accounts:profile'))
	return  HttpResponseRedirect(reverse('accounts:profile'))