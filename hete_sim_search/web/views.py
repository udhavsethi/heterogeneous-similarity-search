from django.shortcuts import render
from django.http import HttpResponse

from subprocess import Popen, PIPE
import os

def auto_complete(request):
	if request.method == 'POST':
		label = request.POST.get('label', 'actor')
		query = request.POST.get('query', '')
		
		p = Popen(["python", "testScript.py", "arg1"], cwd=r"C:\Users\Sony\Desktop\Git\heterogeneous-similarity-search\hete_sim_search\web\scripts", stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()
		return HttpResponse("auto_complete: " + str(out) + str(err))

		# return HttpResponse("label: " + label + " query: " + query)


def top_k_results(request):
	if request.method == 'POST':
		label = request.POST.get('label', 'actor')
		meta_path = request.POST.get('meta_path','AMA')
		k_value = request.POST.get('k_value', '10')
		query = request.POST.get('query', '')

		p = Popen(["python", "testScript.py", "arg1"], cwd=r"C:\Users\Sony\Desktop\Git\heterogeneous-similarity-search\hete_sim_search\web\scripts", stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()
		return HttpResponse("top_k_results: " + str(out) + str(err))