from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from .forms import LoginForm


def index(request):
    return render(request, 'index.html')


@login_required
def graph(request):
    return render(request, 'dashboard.html')


class AtlasLoginView(LoginView):
    template_name = 'auth-signin.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'
