from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from common.extpaginator import ExtPaginator

from .models import Tag, Post, Comment
from .forms import EmailPostForm, CommentForm, PublishForm, PublishMdForm

from actions.utils import create_action
#from taggit.models import Tag


def index(request):  #, tag_slug=None):
	post_list = Post.published.all()

	#tag = None
	#if tag_slug:
	#	tag = get_object_or_404(Tag, slug=tag_slug)
	#	object_list = object_list.filter(tags__in=[tag])
	tag_list = Tag.objects.all()


	paginator = Paginator(post_list, 3)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'page': page, 'posts': posts, 'tag_list': tag_list}

	return render(request, 'blog/index.html', context)





def index_1(request):
	post_list = Post.published.all()

	tag_list = Tag.objects.all()


	paginator = ExtPaginator(post_list, 5, 3)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'page': page, 'posts': posts, 'tag_list': tag_list}

	return render(request, 'blog/index-1.html', context)


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginator_by = 3
	template_name = 'blog/index-1.html'


def tag(request, tag):
	tag = get_object_or_404(Tag, name=str(tag))
	post_list = tag.blog_tags.all()

	tag_list = Tag.objects.all()


	paginator = ExtPaginator(post_list, 5, 3)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'page': page, 'posts': posts, 'tag_list': tag_list, 'tag': tag}

	return render(request, 'blog/tag.html', context)




# Post detail with slug
'''
@login_required
def post(request, year, month, day, post):

	# new = False

	post = get_object_or_404(Post, slug=post, 
                                   status='P',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

	viewed = request.session.get('viewed')

	if not viewed:
		post.views += 1
		post.save()
	
	request.session['viewed'] = True

	comments = post.comments.all().filter(active=True)

	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.name = request.user
			new_comment.save()
	#else:
	comment_form = CommentForm()

	context = {'post': post, 'comments': comments, 'comment_form': comment_form}
	return render(request, 'blog/post.html', context)
'''

# Post detail with id
# @login_required
def post(request, id):
	post = get_object_or_404(Post, id=int(id), status='P')

	if not request.session.get('viewed'):
		post.views += 1
		post.save()
	
	request.session['viewed'] = True

	comments = post.comments.all().filter(active=True)

	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.name = request.user
			new_comment.save()
			return redirect(reverse('blog:post', args=[id,]))
	#else:
	comment_form = CommentForm()

	context = {'post': post, 'comments': comments, 'comment_form': comment_form}
	return render(request, 'blog/post.html', context)



@login_required
@require_POST
@ajax_required
def post_like(request):
	post_id = request.POST.get('post_id')

	if post_id:
		post = get_object_or_404(Post, id=int(post_id))
		post.likes += 1
		post.save()
		return JsonResponse({'count': post.likes})


def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id, status='P')
	sent = False

	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# If your form data does not validate, cleaned_data will only contain the valid fields.
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = "{}<{}> recommends you reading '{}'".format(cd['name'], cd['email'], post.title)
			message = "Read '{}' at {}\n\n{}\'s comments: {}".format(post.title, 
				                                                     post_url,
				                                                     cd['name'],
				                                                     cd['comments'])
			send_mail(subject, message, 'kaikty@163.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()

	return render(request, 'blog/share.html', {'post': post,
		                                            'form': form,
		                                            'sent': sent})


@login_required
def publish(request):
	user = request.user

	# 获取用户设置的编辑器
	try:
		editor = user.settings.settings
	except:
		editor = 'M'

	if editor == 'M':
		if request.method == 'POST':
			form = PublishMdForm(request.POST)
			if form.is_valid():
				new_post = form.save(commit=False)

				new_post.author = request.user
				new_post.save()

				# Adding user actions to the activity stream
				create_action(request.user, '发表了', new_post)

				# 必须save后才能添加manytomany关系
				for tag in form.cleaned_data['tags']:
					new_post.tags.add(tag)

				# 用户后输入的标签
				extra_tags_list = form.cleaned_data['extra_tags']
				
				# get_or_create()
				# 1、If an object is found, get_or_create() returns a tuple of that object and False.
				# 2、If multiple objects are found, get_or_create raises MultipleObjectsReturned.
				# 3、If an object is not found, get_or_create() will instantiate and save a new object, 
				# returning a tuple of the new object and True. The new object will be created 
				# roughly according to this algorithm:
				for exttag in extra_tags_list:
					obj, created = Tag.objects.get_or_create(name=exttag)
					if created:
						new_post.tags.add(obj)
					else:
						try:
							new_post.tags.add(obj)
						except:
							pass

				if new_post.status == 'P':
					return HttpResponseRedirect(reverse("blog:post", args=(new_post.id,)))
				return HttpResponseRedirect(reverse("accounts:mydrafts"))
		else:
			form = PublishMdForm()
		return render(request, 'blog/publish-md.html', {'form': form})

	# 火候未到，未能将其融合为一
	if request.method == 'POST':
		form = PublishForm(request.POST) 
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

			for tag in form.cleaned_data['tags']:
				new_post.tags.add(tag)

			extra_tags_list = form.cleaned_data['extra_tags']

			for exttag in extra_tags_list:
				obj, created = Tag.objects.get_or_create(name=exttag)
				if created:
					new_post.tags.add(obj)
				else:
					try:
						new_post.tags.add(obj)
					except:
						pass
			if new_post.status == 'P':
				return HttpResponseRedirect(reverse("blog:post", args=(new_post.id,)))
			return HttpResponseRedirect(reverse("accounts:mydrafts"))
	else:
		form = PublishForm()
	return render(request, 'blog/publish.html', {'form': form})

	#if request.method == 'POST':
	#	form = PublishMdForm(request.POST) if editor=='M' else PublishForm(request.POST) 
	#	if form.is_valid():
	#		new_post = form.save(commit=False)
	#		new_post.author = request.user
	#		new_post.save()
	#		return HttpResponseRedirect(reverse("blog:post", args=(new_post.id,)))
	#else:
	#	form = PublishMdForm() if editor=='M' else PublishForm()

	#return render(request, 'blog/publish.html', {'form': form})


# 这个功能做的很烂，不知道怎么把原本的内容渲染进表单，shit
@login_required
def edit(request, id):
	post = get_object_or_404(Post, id=int(id))

	# 获取用户设置的编辑器
	try:
		editor = user.settings.settings
	except:
		editor = 'M'

	if request.method == "POST":
		if editor == 'M':
			form = PublishMdForm(request.POST, instance=post)
		else:
			form = PublishForm(request.POST, instance=post)

		if form.is_valid():
			form.save()
	else:
		form = PublishForm(instance=post)

	return render(request, 'blog/edit.html', {'form': form})