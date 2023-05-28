from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

class new_post(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

def index(request):
    # autheticated users view their profile page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user", kwargs={"id": request.user.id}))
    # others are prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user(request, id):
    if request.method == "GET":
        # takes user id argument and displays their profile
        try:
            profile_user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("user", kwargs={"id": request.user.id}))

        posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

        if profile_user != request.user:
            try:
                UserFollowing.objects.get(user=profile_user, follower_user=request.user)
                follow = True
            except UserFollowing.DoesNotExist:
                follow = False

            return render(request, "network/user.html", {
                "user": profile_user,
                "posts": posts,
                "follows": follow
            })
        else:
            return render(request, "network/user.html", {
                "user": profile_user,
                "posts": posts
            })

def follow(request, id):
    # follow a user corresponding to the user id
    try:
        user_tofollow = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    try:
        follow = UserFollowing.objects.get(user=user_tofollow, follower_user=request.user)
        follow.delete()
    except UserFollowing.DoesNotExist:
        follow = UserFollowing.objects.create(user=user_tofollow, follower_user=request.user)
        follow.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return HttpResponse(status=204)

from django.core.paginator import Paginator

def posts(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # create post
            content = request.POST['content']
            user = request.user
            post = Post.objects.create(content=content, user=user)
            post.save()

            return HttpResponseRedirect(reverse("posts"))
        else:
            posts = Post.objects.order_by('-timestamp')

            paginator = Paginator(posts, 10)
            page = request.GET.get('page', 1)

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            likes = Like.objects.filter(like_user=request.user)
            liked = []
            for post in posts:
                for like in likes:
                    if like in post.likes.all():
                        liked.append(post)
            # paginator to display 10 posts at a time

            return render(request, "network/posts.html", {
                "form": new_post(),
                "posts": posts,
                "liked": liked
            })
    else:
        return HttpResponseRedirect(reverse("login"))

def get_time(post):
    return post.timestamp

def following(request):
    if request.user.is_authenticated:
        # get posts by users that are being followed
        users = request.user.following.all()
        likes = Like.objects.filter(like_user=request.user)
        # users is a queryset of UserFollowing objects

        # loops through users and their posts and compiles them in a list
        posts = []
        liked = []
        for user in users:
            user_posts = Post.objects.filter(user_id=user.user.id)
            for post in user_posts:
                posts.append(post)
                for like in likes:
                    if like in post.likes.all():
                        liked.append(post)

        posts.sort(key=get_time, reverse=True)

        paginator = Paginator(posts, 10)
        page = request.GET.get('page', 1)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)


        return render(request, "network/posts.html", {
            "posts": posts,
            "liked": liked
        })

@csrf_exempt
def edit(request, id):
    #gets form data as new content of post
    new_content = request.POST["content"]

    post = Post.objects.get(pk=id)
    post.content = new_content
    post.save()

    return HttpResponseRedirect(reverse('posts'))

def like(request, id):
    # like a post corresponding to the post id
    try:
        post = Post.objects.get(pk=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    try:
        like = Like.objects.get(post=post, like_user=request.user)
        like.delete()
    except Like.DoesNotExist:
        like = Like.objects.create(post=post, like_user=request.user)
        like.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
