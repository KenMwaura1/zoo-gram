from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from z_gram.forms import RegisterForm, UserPostForm
from z_gram.models import UserPost


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
    images = UserPost.objects.all()
    users = User.objects.exclude(id=request.user.id)
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
        'images': images,
        'form': form,
        'users': users,

    }
    return render(request, 'z-gram/home.html', params)
