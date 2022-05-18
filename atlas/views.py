from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import LoginForm
from .models import Cmn, Ai
from .serializers import CmnSerializer


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def table(request):
    return render(request, 'table.html')


class AtlasLoginView(LoginView):
    template_name = 'auth-signin.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'


# api
@api_view(['GET'])
def api_cmn(request):
    if request.method == 'GET':
        temp = Cmn.objects.all()
        serializer = CmnSerializer(temp, many=True)
        return Response(serializer.data)
