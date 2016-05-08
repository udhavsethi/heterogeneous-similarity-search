from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

from subprocess import Popen, PIPE
import os


def auto_complete(request):
    if request.method == 'POST' or request.method == 'GET':
        label = request.POST.get('label', 'actor')
        query = request.POST.get('query', 'tr')
        
        scriptPath = os.getcwd()+r"\web\scripts"
        p = Popen(["python", "autoComplete.py", label, query], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        return HttpResponse(out)


def top_k_results(request):
    if request.method == 'POST' or request.method == 'GET' :
        
        #Extract Values from POST variables
        label = request.POST.get('label', 'actor')
        meta_path = request.POST.get('meta_path','AMA')
        k_value = request.POST.get('k_value', '10')
        query = request.POST.get('query', 'Pauli Maar')
        
        #Run coresponding script and return data
        scriptPath = os.getcwd()+r"\web\scripts"
        p = Popen(["python", meta_path+".py", query, k_value], cwd=scriptPath, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        response = HttpResponse(out)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
        # return HttpResponse(out)