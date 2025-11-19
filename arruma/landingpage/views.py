from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    context = {}
    return render(request, 'landingpage/index.html', context)


def how_it_works(request):
    return render(request, 'landingpage/how_it_works.html')


def terms_of_use(request):
    return render(request, 'landingpage/terms_of_use.html')


def privacy_policy(request):
    return render(request, 'landingpage/privacy_policy.html')