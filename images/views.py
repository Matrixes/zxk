from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count

from .forms import ImageCreateForm
from .models import Image

from common.decorators import ajax_required
from actions.utils import create_action


def index(request):
	images = Image.objects.all().order_by('-created')

	# 根据受欢迎程度对图片排序, 当然这个代价太高，不如在models中添加一个field来存储
	# images_by_popularity = Image.objects.annotate(total_likes=Count('users_like')).order_by('-total_likes')
	images_by_popularity = Image.objects.order_by('-total_likes')
	
	return render(request, 'images/index.html', {'images': images})


@login_required
def image_create(request):
	if request.method == 'POST':
		form = ImageCreateForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()

			# Adding user actions to the activity stream
			create_action(request.user, 'bookmarked image', new_item)

			messages.success(request, 'Image added successfully')
			return redirect(new_item.get_absolute_url())
	else:
		form = ImageCreateForm(data=request.GET)
	return render(request, 'images/create.html', {'form': form})


def image_detail(request, id):
	image = get_object_or_404(Image, id=id)
	return render(request, 'images/detail.html', {'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=int(image_id))
			if action == 'like':
				image.users_like.add(request.user)
				create_action(request.user, '点赞了', image)
			else:
				image.users_like.remove(request.user)
				create_action(request.user, '取消点赞了', image)
			return JsonResponse({'status': 'ok'})
		except:
			pass
	return JsonResponse({'status': 'ko'})
