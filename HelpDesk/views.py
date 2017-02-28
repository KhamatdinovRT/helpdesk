from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Structure, Request, Users, RequestStatus, RequestTasks, TaskList
from .forms import RequestForm
import json
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms import formset_factory
from django.shortcuts import get_object_or_404


def request_view(request):
    matches = Request.objects.all()
    form = RequestForm ()
    return render(request, 'request.html', {'form': form, 'matches': matches})

def request_edit(request, request_id):
    # print (request.POST['request_id'])
    request_from_helpdesk = get_object_or_404(Request, number=request_id)
    data = dict()
    
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=request_from_helpdesk)
        if form.is_valid():
            form.save()
            requests = Request.objects.all()
            data['form_is_valid'] = True
            data['html_book_list'] = render_to_string('requests_list.html', {'matches': requests})        
            return JsonResponse(data)
    else:
        tasks = RequestTasks.objects.filter(request=request_id).values_list('tasklist', flat=True) 
        form = RequestForm(instance=request_from_helpdesk, initial={'tasks': list(tasks)})
    context = {'form': form}
    
    data['html_form'] = render_to_string('modal_edit_form.html', context, request=request)
    return JsonResponse(data)
