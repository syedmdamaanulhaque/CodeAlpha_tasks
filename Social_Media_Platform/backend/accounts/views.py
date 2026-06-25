from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from posts.models import Post
from interactions.models import Follow
from .models import Profile


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("/")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def profile(request, user_id):

    profile_user = get_object_or_404(
        User,
        id=user_id
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    return render(
        request,
        "profile.html",
        {
            "profile_user": profile_user,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
        }
    )


@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES[
                "profile_picture"
            ]

        profile.bio = request.POST.get(
            "bio",
            profile.bio
        )

        profile.save()

        return redirect(
            f"/profile/{request.user.id}/"
        )

    return render(
        request,
        "edit_profile.html",
        {
            "profile": profile
        }
    )