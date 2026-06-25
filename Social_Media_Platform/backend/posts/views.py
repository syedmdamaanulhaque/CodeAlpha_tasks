from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from interactions.models import Comment, Follow


def home(request):
    posts = Post.objects.all().order_by('-created_at')

    following_users = []

    if request.user.is_authenticated:
        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list(
            'following_id',
            flat=True
        )

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'following_users': following_users,
        }
    )


@login_required
def create_post(request):

    if request.method == "POST":

        caption = request.POST.get("caption")
        image = request.FILES.get("image")

        Post.objects.create(
            user=request.user,
            caption=caption,
            image=image
        )

        return redirect('/')

    return render(
        request,
        'create_post.html'
    )