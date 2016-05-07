from django.shortcuts import render
from django.http import HttpResponse

from subprocess import Popen, PIPE
import os

def auto_complete(request):
    # if request.method == 'POST':
    label = request.POST.get('label', 'actor')
    query = request.POST.get('query', '')
    
    scriptPath = os.getcwd()+r"\web\scripts"
    p = Popen(["python", "autoComplete.py", label, query], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return HttpResponse(out)


def top_k_results(request):
    # if request.method == 'POST':
    label = request.POST.get('label', 'actor')
    #TODO: remove testScript and put AMA
    meta_path = request.POST.get('meta_path','testScript')
    k_value = request.POST.get('k_value', '10')
    query = request.POST.get('query', 'George Clooney')
    
    scriptPath = os.getcwd()+r"\web\scripts"
    p = Popen(["python", meta_path+".py", query, k_value], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
    # p = Popen(["python", meta_path+".py", query, k_value], cwd=r"C:\Users\Sony\Desktop\Git\heterogeneous-similarity-search\hete_sim_search\web\scripts", stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return HttpResponse(out)