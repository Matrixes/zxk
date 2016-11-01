# -*- coding:utf8 -*-

import re
from django import forms

from pagedown.widgets import PagedownWidget, AdminPagedownWidget

from .models import Comment, Post, Tag


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
            'body': PagedownWidget(template="blog/pagedown.html", css=("blog/pagedown-comment.css", )),
        }


class PublishForm(forms.ModelForm):
    extra_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def clean_extra_tags(self):
        extra_tags = self.cleaned_data['extra_tags']

        tag_list = re.split(r'[,;\s]\s*', extra_tags)

        return [i.strip() for i in tag_list]
        
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'id': 'woca', 'class': 'form-control'}),
        }




class PublishMdForm(forms.ModelForm):
    # atextfield = forms.CharField(widget=PagedownWidget())
    # anothertextfield = forms.CharField(widget=PagedownWidget())

    extra_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 当已经保存的标签不够时，定义一个标签输入框，使用逗号和分号隔开
    def clean_extra_tags(self):
        extra_tags = self.cleaned_data['extra_tags']

        tag_list = re.split(r'[,;\s]\s*', extra_tags)

        '''
        for tag in tag_list:
            if Tag.objects.filter(name=tag):
                raise forms.ValidationError("标签{}已经存在".format(tag))
        '''

        return [i.strip() for i in tag_list]

    
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'body': PagedownWidget(template="blog/pagedown.html", css=('blog/pagedown-publish.css', )),
        }
            