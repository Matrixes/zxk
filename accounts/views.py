# -*- cpding:utf8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
import json
from requests_oauthlib import OAuth2Session

client_id = '9890f2416a5ee83e8da8'
client_secret = '9ad5f139646112dd848a295b1b708730fe4152f2'

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

redirect_uri = "http://127.0.0.1:8000/accounts/github_auth"
scope = []

def github_login(request):
	github = OAuth2Session(client_id)  #, redirect_uri=redirect_uri, scope=scope)

	# Redirect user to GitHub for authorization
	authorization_url, state = github.authorization_url(authorization_base_url)

	request.session['oauth_state'] = state

	print(authorization_url)
	return HttpResponseRedirect(authorization_url)


def github_auth(request):
	github = OAuth2Session(client_id, state=request.session['oauth_state'])
	token = github.fetch_token(token_url, 
		                       client_secret=client_secret, 
		                       authorization_response=redirect_uri)
	r = github.get('https://api.github.com/user')
	print(r.content)