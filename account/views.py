# -*- cpding:utf8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

from django.contrib.auth.models import User
from .models import Profile
from blog.models import Post, Comment


@login_required
def dashboard(request):
	profile = Profile.objects.get(user=request.user)
	posts = Post.objects.filter(author=request.user)
	comments = Comment.objects.filter(name=request.user)
	return render(request, 'account/dashboard.html', 
		                   {'profile': profile,
		                    'posts': posts,
		                    'comments': comments})


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, 
			                           data=request.POST,
			                           files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, '成功啦')
		else:
			messages.error(request, '失败了')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 
		         'account/edit.html', 
		         {'user_form': user_form, 
		          'profile_form': profile_form})