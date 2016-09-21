# -*- coding:utf8 -*-


from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
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

"""
You can provide a clean_<fieldname>() method to any of your form fields in
order to clean the value or raise form validation errors for the specific field. Forms
also include a general clean() method to validate the entire form, which is useful to
validate fields that depend on each other.

Django also provides a UserCreationForm form that you can use, which resides in
django.contrib.auth.forms and is very similar to the one we have created.
"""


from .models import Profile


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('nickname', 'birthday', 'photo')