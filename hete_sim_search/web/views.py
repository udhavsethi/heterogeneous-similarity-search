from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def top_k_results(request):
	return HttpResponse("Working.")