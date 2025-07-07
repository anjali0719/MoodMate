from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def test_view(request):
    return HttpResponse("This is for testing purpose")