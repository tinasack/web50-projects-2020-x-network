from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like
from django.db.models import Count


def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()

    paginate = Paginator(allPosts, 10)
    pageNumber = request.GET.get('page')
    postsOfPage = paginate.get_page(pageNumber)

    allLikes = Like.objects.all()
    myLikedPosts = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                myLikedPosts.append(like.post.id)
    except:
        myLikedPosts = []


    countLikes = Like.objects.values('post_id').order_by('post_id').annotate(count=Count('post_id'))

    return render(request, "network/index.html", {
        "postsOfPage": postsOfPage,
        "myLikes": myLikedPosts,
        "countLikes": countLikes
    })


def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allUserPosts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user=user)
    follower = Follow.objects.filter(followed=user)

    try:
        checkFollow = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    paginate = Paginator(allUserPosts, 10)
    pageNumber = request.GET.get('page')
    postsOfPage = paginate.get_page(pageNumber)

    allLikes = Like.objects.all()
    myLikedPosts = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                myLikedPosts.append(like.post.id)
    except:
        myLikedPosts = []

    countLikes = Like.objects.values('post_id').order_by('post_id').annotate(count=Count('post_id'))

    return render(request, "network/profile.html", {
        "postsOfPage": postsOfPage,
        "username": user.username,
        "following": following,
        "follower": follower,
        "isFollowing": isFollowing,
        "profile": user,
        "myLikes": myLikedPosts,
        "countLikes": countLikes
    })

def follow(request):
    follow = request.POST['follow']
    currentUser = User.objects.get(pk=request.user.id)
    followUserData = User.objects.get(username=follow)
    follower = Follow(user=currentUser, followed=followUserData)
    follower.save()
    userID = followUserData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': userID}))

def unfollow(request):
    unfollow = request.POST['unfollow']
    currentUser = User.objects.get(pk=request.user.id)
    unfollowUserData = User.objects.get(username=unfollow)
    follower = Follow.objects.get(user=currentUser, followed=unfollowUserData)
    follower.delete()
    userID = unfollowUserData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': userID}))

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followedUsers = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by('id').reverse()

    followedUserPosts = []

    for post in allPosts:
        for user in followedUsers:
            if user.followed == post.user:
                followedUserPosts.append(post)

    paginate = Paginator(followedUserPosts, 10)
    pageNumber = request.GET.get('page')
    postsOfPage = paginate.get_page(pageNumber)

    allLikes = Like.objects.all()
    myLikedPosts = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                myLikedPosts.append(like.post.id)
    except:
        myLikedPosts = []

    countLikes = Like.objects.values('post_id').order_by('post_id').annotate(count=Count('post_id'))

    return render(request, "network/following.html", {
        "postsOfPage": postsOfPage,
        "myLikes": myLikedPosts,
        "countLikes": countLikes
    })

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        editPost = Post.objects.get(pk=post_id)
        editPost.content = data["content"]
        editPost.save()
    return JsonResponse({"message": "successful change", "data": data["content"]}) 


def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes = post.likes + 1
    likes = post.likes
    post.save()
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    return JsonResponse({"message": "Like added", "likes": likes})


def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes = post.likes - 1
    likes = post.likes
    post.save()
    user = User.objects.get(pk=request.user.id)
    deleteLike = Like.objects.filter(user=user, post=post)
    deleteLike.delete()
    return JsonResponse({"message": "Like deleted", "likes": likes})

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
