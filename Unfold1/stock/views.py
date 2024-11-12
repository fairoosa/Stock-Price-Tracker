from django.shortcuts import render
from django.views import generic
from bs4 import BeautifulSoup
import requests
from .models import Stock

class HomePage(generic.ListView):
    template_name = "home.html"
    model = Stock

    def get_queryset(self):
        print("data : ", Stock.objects.all())
        return Stock.objects.order_by('-updated_at')


