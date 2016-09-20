# -*- coding:utf8 -*-


from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25, label="名字")
	email = forms.EmailField(label="您的邮箱")
	to = forms.EmailField(label="分享邮箱")
	comments = forms.CharField(required=False, widget=forms.Textarea, label="评论")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)