from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from django.utils.timezone import now
from django.conf import settings


def filter_queryset(posts):
    return posts.filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
        )

def index(request):
    post_list = filter_queryset(
            Post.objects.select_related(
                'author',
                'location',
                'category'
            )
        )[:settings.POST_COUNT]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        filter_queryset(
            Post.objects.select_related(
                'author', 'category', 'location'
            )
        ),
        id=id
        )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lt=now()
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
