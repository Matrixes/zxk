# -*- coding:utf8 -*-


from django import forms
from .models import UserProfile, UserSettings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		un = self.cleaned_data['username']
		if len(un) < 3:
			raise forms.ValidationError("Too short")
		return un


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label="密  码", widget=forms.PasswordInput)
	password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("密码不一致")
		return cd['password2']


# Edit profile
# failed to render the data of form to forms
"""
class ProfileForm(forms.Form):
	username = forms.CharField()
	nickname = forms.CharField()
	email = forms.EmailField()
	phone = forms.CharField()
	website = forms.URLField()
	birthday = forms.DateField()
	photo = forms.ImageField()


"""

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		if User.objects.filter(username=username):
			# There is a bug: when you update other profile, Error also raised
			# raise forms.ValidationError('username alraedy exists.')
			pass
		return username


class ProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('nickname', 'phone', 'website', 'birthday', 'photo')
		widgets = {
			'birthday': forms.DateInput,
		}


class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput)
	new_password = forms.CharField(widget=forms.PasswordInput)
	new_password2 = forms.CharField(widget=forms.PasswordInput)

	def clean_new_password2(self):
		new_password = self.cleaned_data['new_password']
		new_password2 = self.cleaned_data['new_password2']
		if len(new_password) < 6:
			raise forms.ValidationError("Password too short")
		return new_password
		if new_password != new_password2:
			raise forms.ValidationError("Password does not match.")
		return new_password2


class UserSettingsForm(forms.ModelForm):
	class Meta:
		model = UserSettings
		fields = ('settings',)