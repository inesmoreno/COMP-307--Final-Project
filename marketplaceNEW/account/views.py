from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import forms

@login_required
def info(request):
    #if user is logged in, show account info otherwise prompt a log in
    if request.user.username:
        
        return render(request,'account/account_info.html')
    return render(request,'account/login.html')

def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
              user = User.objects.create_user(
                form.cleaned_data['username'], 
                email=form.cleaned_data['email'], 
                password=form.cleaned_data['password'])
              return HttpResponseRedirect(reverse('account:login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'account/signup.html', context)

def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('listing:list'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'account/login.html', context)

def do_logout(request):
    #if request.user.is_authenticated:
        #channel_layer = get_channel_layer()
        #async_to_sync(channel_layer.group_send)(request.user.username, {
            #'type': 'logout_message',
            #'message': 'Disconnecting. You logged out from another browser or tab.'})
      
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))
    