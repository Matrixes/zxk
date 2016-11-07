# -*- coding:utf8 -*-


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import UserProfile, UserSetting


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		un = self.cleaned_data['username']
		if len(un) < 2:
			raise forms.ValidationError("用户名错误")
		return un


###### Edit profile Start ######
class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		if User.objects.filter(username=username):
			pass
		return username

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('nickname', 'website', 'birthday', 'introduce', 'photo')
		widgets = {
			'birthday': forms.DateInput,
		}

###### Edit profile End ######

class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput)
	new_password = forms.CharField(widget=forms.PasswordInput)
	new_password2 = forms.CharField(widget=forms.PasswordInput)

	def clean_new_password2(self):
		new_password = self.cleaned_data['new_password']
		new_password2 = self.cleaned_data['new_password2']

		if len(new_password) < 6:
			raise forms.ValidationError("Password too short")

		if new_password != new_password2:
			raise forms.ValidationError("Password does not match.")
		return new_password2


# 用户设置表单
class UserSettingForm(forms.ModelForm):
	class Meta:
		model = UserSetting
		fields = ('setting', 'domain')

		widgets = {
			
		}


# 用户注册表单
class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label="密  码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("密码不一致")
		return cd['password2']