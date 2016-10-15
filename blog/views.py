from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .models import Tag, Post, Comment
from .forms import EmailPostForm, CommentForm, PublishForm

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


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginator_by = 3
	template_name = 'blog/post/list.html'


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


def post_like(request):
	post_id = None
	if request.method == 'GET':
		post_id = request.GET.get('post_id')

	if post_id:
		post = get_object_or_404(Post, id=int(post_id))
		post.likes += 1
		post.save()

	return HttpResponse(post.likes)


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

	return render(request, 'blog/post/share.html', {'post': post,
		                                            'form': form,
		                                            'sent': sent})

def tag(request, tag):
	tag = get_object_or_404(Tag, name=str(tag))
	post_list = tag.blog_tags.all()

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

	return render(request, 'blog/tag.html', context)


@login_required
def publish(request):
	if request.method == 'POST':
		pass
	else:
		form = PublishForm()
	return render(request, 'blog/publish.html', {'form': form})