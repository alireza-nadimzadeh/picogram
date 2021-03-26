from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from django.contrib.auth.models import User
from post.models import Post
from .models import Profile


def u_profile(request, pk):
    user1 = request.user

    user2 = User.objects.get(pk=pk)
    profile2 = Profile.objects.get(user=user2)

    # if the target user is the logged in user take them to their own profile form
    if user1 == user2:
        return profile(request)

    posts = Post.objects.filter(author=user2)
    followers = profile2.followers.all()
    followed = False
    if user1 in followers:
        followed = True
    context = {
        'posts': posts,
        'user1': user1,
        'user2': user2,
        'followed': followed,


    }
    return render(request, 'user/u_profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Good! You can now log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def follow_user(request, pk):
    user1 = request.user
    profile1 = Profile.objects.get(user=user1)
    user2 = User.objects.get(pk=pk)
    profile2 = Profile.objects.get(user=user2)
    if user1 != user2:
        profile2.followers.add(user1)
        profile1.following.add(user2)
    return redirect('u-profile', pk)


def unfollow_user(request, pk):
    user1 = request.user
    profile1 = Profile.objects.get(user=user1)
    user2 = User.objects.get(pk=pk)
    profile2 = Profile.objects.get(user=user2)
    if user1 != user2:
        profile2.followers.remove(user1)
        profile1.following.remove(user2)
    return redirect('u-profile', pk)


@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
    }

    return render(request, 'user/profile.html', context)
