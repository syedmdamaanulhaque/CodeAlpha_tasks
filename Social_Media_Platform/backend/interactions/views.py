from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from posts.models import Post
from .models import Comment, Like, Follow


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("comment")

        Comment.objects.create(
            user=request.user,
            post=post,
            text=text
        )

    return redirect('/')


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    existing_like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if existing_like.exists():
        existing_like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('/')


@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return redirect('/')

    existing_follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if existing_follow.exists():
        existing_follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

    return redirect('/')