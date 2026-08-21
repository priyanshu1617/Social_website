import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image


def get_redis():
    """Lazy Redis connection — avoids settings access at import time."""
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            from actions.utils import create_action
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'images/image/create.html',
        {'section': 'images', 'form': form},
    )


@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = 0
    try:
        r = get_redis()
        # Increment total views in Redis
        total_views = r.incr(f'image:{image.id}:views')
        # Increment image ranking in sorted set
        r.zincrby('image_ranking', 1, image.id)
    except Exception:
        # Redis unavailable — continue without view tracking
        pass
    return render(
        request,
        'images/image/detail.html',
        {
            'section': 'images',
            'image': image,
            'total_views': total_views,
        },
    )


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                from actions.utils import create_action
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            # Update denormalized total_likes count
            image.total_likes = image.users_like.count()
            image.save(update_fields=['total_likes'])
            return JsonResponse({'status': 'ok', 'total_likes': image.total_likes})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # AJAX request: return empty response when no more pages
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            'images/image/list_ajax.html',
            {'section': 'images', 'images': images},
        )
    return render(
        request,
        'images/image/list.html',
        {'section': 'images', 'images': images},
    )


@login_required
def image_ranking(request):
    most_viewed = []
    try:
        r = get_redis()
        # Get image ranking dictionary from Redis (top 10 most viewed)
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        # Get most viewed images sorted by ranking
        most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    except Exception:
        # Redis unavailable — show empty ranking
        pass
    return render(
        request,
        'images/image/ranking.html',
        {'section': 'images', 'most_viewed': most_viewed},
    )
