from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import RedirectView

from z_gram.forms import RegisterForm, UserPostForm, UpdateUserForm, UpdateUserProfileForm, CommentForm
from z_gram.models import UserPost, Follow, UserProfile

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
    """
    main view that handles rendering home page
    """
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
    """
    route to own user profile
    """
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
    """
    route to return another users profile
    """
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        return redirect('profile', username=request.user.username)
    user_posts = user_profile.userprofile.userposts.all()
    followers = Follow.objects.filter(followed=user_profile.userprofile)
    follow_status = None
    print(request.user, 'User')
    for follower in followers:
        follow_status = request.user == follower.follower

    params = {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'z-gram/user_profile.html', params)


@login_required(login_url='login')
def post_comment(request, id):
    """
    route to create new comments
    """
    image = get_object_or_404(UserPost, pk=id)
    is_liked = bool(image.likes.filter(id=request.user.id).exists())
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            save_comment = form.save(commit=False)
            save_comment.post = image
            save_comment.user = request.user.userprofile
            save_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'z-gram/single_post.html', params)


class LikePost(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get('id')
        object = get_object_or_404(UserPost, pk=id)
        url = object.get_absolute_url()
        user = self.request.user
        if user in object.likes.all():
            object.likes.remove(user)
        else:
            object.likes.add(user)
        return url


def like_post(request):
    # image = get_object_or_404(Post, id=request.POST.get('image_id'))
    image = get_object_or_404(UserPost, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
    else:
        image.likes.add(request.user)
    is_liked = False
    params = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('z-gram/like_page.html', params, request=request)
        return JsonResponse({'form': html})


def follow(request, to_follow):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(pk=to_follow)
        follow = Follow(follower=request.user.userprofile, followed=user_profile)
        follow.save()
        return redirect('user_profile', user_profile.user.username)


def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(pk=to_unfollow)
        unfollow = Follow.objects.filter(follower=request.user.userprofile, followed=user_profile)
        unfollow.delete()
        return redirect('user_profile', user_profile.user.username)


@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = UserProfile.search_profile(name)
        print(results)
        message = f'{name}'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'z-gram/results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'z-gram/results.html', {'message': message})
