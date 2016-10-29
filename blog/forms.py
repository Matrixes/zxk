# -*- coding:utf8 -*-


from django import forms

from .models import Comment, Post


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25, label="名字")
	email = forms.EmailField(label="您的邮箱")
	to = forms.EmailField(label="分享邮箱")
	comments = forms.CharField(required=False, widget=forms.Textarea, label="评论")


from pagedown.widgets import PagedownWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


        widgets = {
            'body': PagedownWidget(template="blog/pagedown.html", css=("blog/pagedown.css", )),
        }


class PublishForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'id': 'woca', 'class': 'form-control'}),
        }


from pagedown.widgets import PagedownWidget

class PublishMdForm(forms.ModelForm):
    # atextfield = forms.CharField(widget=PagedownWidget())
    # anothertextfield = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'body': PagedownWidget,
        }