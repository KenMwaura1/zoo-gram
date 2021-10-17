from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from z_gram.forms import RegisterForm, UserPostForm, UpdateUserForm, UpdateUserProfileForm
from z_gram.models import UserPost, Follow

"""def home(request):
    return render(request, 'z-gram/home.html')"""


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'django_registration/registration_form.html', {'form': form})


@login_required(login_url='login')
def home(request):
    all_images = UserPost.objects.all()
    all_users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = UserPostForm()
    params = {
        'images': all_images,
        'users': all_users,
        'form': form,
    }
    return render(request, 'z-gram/home.html', params)


@login_required(login_url='login')
def profile(request, username):
    images = request.user.userprofile.userposts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.userprofile)
    params = {
        'user_form': user_form,
        'profile_form': profile_form,
        'images': images,

    }
    return render(request, 'z-gram/profile.html', params)


@login_required(login_url='login')
def user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        return redirect('profile', username=request.user.username)
    user_posts = user_profile.userprofile.userposts.all()
    followers = Follow.objects.filter(followed=user_profile.userprofile)
    follow_status = None
    for follower in followers:
        follow_status = request.user.userprofile == follower.follower
    params = {
        'user_prof': user_profile,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'z-gram/user_profile.html', params)
