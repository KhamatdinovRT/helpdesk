from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Structure, Request, Users, RequestStatus, RequestTasks, TaskList, TempRequest
from .forms import RequestForm, WorkerRequestForm, ClientRequestForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test  
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from ast import literal_eval
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate (queryset, request):  
    if request.method == 'GET':
        try:
            page = request.GET.get('page')
        except:
            page = 1            
    else:
        try:
            page = request.POST.get('page')            
        except:
            page = 1
    paginate_by = 18
    paginator = Paginator(queryset, paginate_by)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    
    if (paginator.num_pages>10):
        current_page = paginated_queryset.number 
        max_index = paginator.num_pages

        pages_to_display = 5
        step = pages_to_display//2
        if (current_page - 1 < pages_to_display+1 ):
            start_index = 0
        else:
            start_index = current_page - (step + 1) if current_page >= (step + 1)  else 0
        if (max_index - current_page < pages_to_display+1):
            end_index = max_index
        else:
            end_index = current_page + step if current_page <= max_index - step else max_index
            
        page_range = paginator.page_range[start_index:end_index]
    else:
        page_range = paginator.page_range  
    return {'matches':paginated_queryset, 'page_range':page_range, 'num_pages':paginator.num_pages}

def in_group_worker(user):
    if user:
        return Group.objects.get(name='worker') in user.groups.all()
    return False

# @login_required(login_url='login')
# @permission_required('HelpDesk.add_tasklist', raise_exception=True)
# @user_passes_test(lambda u: Group.objects.get(name='worker') in u.groups.all(), login_url='login' )
# @user_passes_test(in_group_chief, login_url='access' )
def request_view(request):
    requests = Request.objects.order_by('-number')
    context = paginate (requests, request)
    return render(request, 'request.html', context)

def temp_requests_view(request):
    temp_requests = TempRequest.objects.order_by('-number')
    context = paginate (temp_requests, request)
    context["is_temp_requests_page"] = True
    return render(request, 'request.html', context)

def save_request_form(request, form, requests, list_template_name, form_template_name):
    data = dict()   
    if request.method == 'POST':
        if form.is_valid():
            print ('''''''''''''''valid''''''''''''''')
            form.save()
            # requests = Request.objects.order_by('-number')
            context = paginate (requests, request)
            data['form_is_valid'] = True
            data['html_book_list'] = render_to_string(list_template_name, context) 
        else:
            data['form_is_valid'] = False 
            # context = {'form': form}
            # data['html_form'] = render_to_string(form_template_name, context, request=request)
            print (form.errors) 
    else:
        context = {'form': form}
        data['html_form'] = render_to_string(form_template_name, context, request=request)
    return JsonResponse(data)    

def create_request_from_temp(request, request_id):
    temp_request_from_helpdesk = get_object_or_404(TempRequest, number=request_id) 
    if request.method == 'POST':
        form = RequestForm(request.POST)
        # temp_request_from_helpdesk.delete()
    else:
        form = RequestForm(instance=temp_request_from_helpdesk, initial={'tasks': literal_eval(temp_request_from_helpdesk.tasks)})
    requests = TempRequest.objects.order_by('-number')    
    return save_request_form(request, form, requests, 'temp_requests_list.html','modal_create_form.html')

def request_edit(request, request_id):
    request_from_helpdesk = get_object_or_404(Request, number=request_id)
    requests = Request.objects.order_by('-number')

    if request.method == 'POST':
        if in_group_worker(request.user):
            form = WorkerRequestForm(request.POST, instance=request_from_helpdesk)
        else:
            form = RequestForm(request.POST, instance=request_from_helpdesk)
    else:
        tasks = RequestTasks.objects.filter(request=request_id).values_list('tasklist', flat=True)
        if in_group_worker(request.user):
            form = WorkerRequestForm(instance=request_from_helpdesk, initial={'tasks': list(tasks)})
            print ('worker')
        else:
            form = RequestForm(instance=request_from_helpdesk, initial={'tasks': list(tasks)})
    return save_request_form(request, form, requests, 'requests_list.html','modal_edit_form.html')


def delete_request_from_temp(request, request_id, list_template_name="temp_requests_list.html"):
    data=dict()
    if request.method == 'DELETE':
        temp_request_from_helpdesk = get_object_or_404(TempRequest, number=request_id)   
        print(temp_request_from_helpdesk) 
        temp_request_from_helpdesk.delete()
        requests = TempRequest.objects.order_by('-number')    
        context = paginate (requests, request)  
        data['form_is_valid'] = True
        data['html_book_list'] = render_to_string(list_template_name, context)
    return JsonResponse (data)

def index(request):
    form = ClientRequestForm()
    return render(request, 'index.html', {'form': form})


def create_request(request):
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            temp_request = TempRequest.objects.create(
                client=request.POST["client"], 
                structure = request.POST["structure"], 
                office = request.POST["office"],
                tasks = request.POST.getlist ("tasks"),
                phone_number = request.POST["phone_number"],
                comments = request.POST["comments"]
            )
            return render (request, 'request_created.html')
    return render(request, 'index.html', {'form': form})