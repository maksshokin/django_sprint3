from django.shortcuts import get_object_or_404, render
from blog.models import Post
from django.utils.timezone import now


def index(request):
    post_list = Post.objects.select_related(
        'author',
        'location',
        'category'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        ),
        id=id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category):
    context = {
        'category': category,
    }
    return render(request, 'blog/category.html', context)
