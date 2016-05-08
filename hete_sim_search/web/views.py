from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

from subprocess import Popen, PIPE
import os

# def home(request):
#     template = loader.get_template('web/index.html')
#     return HttpResponse(template.render)

def auto_complete(request):
    # if request.method == 'POST':
    label = request.POST.get('label', 'actor')
    query = request.POST.get('query', '')
    
    scriptPath = os.getcwd()+r"\web\scripts"
    p = Popen(["python", "autoComplete.py", label, query], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return HttpResponse(out)


def top_k_results(request):
    if request.method == 'POST' or request.method == 'GET' :
        label = request.POST.get('label', 'actor')
        meta_path = request.POST.get('meta_path','AMA')
        k_value = request.POST.get('k_value', '2')
        query = request.POST.get('query', 'Hitanshu Arora')  
        
        scriptPath = os.getcwd()+r"\web\scripts"
        p = Popen(["python", meta_path+".py", query, k_value], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
        # p = Popen(["python", meta_path+".py", query, k_value], cwd=r"C:\Users\Sony\Desktop\Git\heterogeneous-similarity-search\hete_sim_search\web\scripts", stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        response = HttpResponse(out)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
        # return HttpResponse(out)