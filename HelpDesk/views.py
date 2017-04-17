from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Structure, Request, Users, RequestStatus, RequestTasks, TaskList, TempRequest
from .forms import RequestForm, WorkerRequestForm, ClientRequestForm
from django.contrib.auth.decorators import login_required, user_passes_test  
from django.http import Http404
from django.http import JsonResponse
from ast import literal_eval
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

def is_superuser(user):
    if user:
        return user.is_superuser
    return False


@login_required
def request_view(request):
    requests = Request.objects.order_by('-number')
    context = paginate (requests, request)
    return render(request, 'request.html', context)

@login_required
@user_passes_test(is_superuser)
def temp_requests_view(request):
    temp_requests = TempRequest.objects.order_by('-number')
    context = paginate (temp_requests, request)
    context["is_temp_requests_page"] = True
    return render(request, 'request.html', context)

@login_required
@user_passes_test(is_superuser)
def create_request_from_temp(request, request_id):
    data = dict ()
    temp_request_from_helpdesk = get_object_or_404(TempRequest, number=request_id)     
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            temp_request_from_helpdesk.delete()
            requests = TempRequest.objects.order_by('-number')
            context = paginate (requests, request)
            data['form_is_valid'] = True
            data['html_book_list'] = render_to_string('temp_requests_list.html', context)    
        else:
            data['form_is_valid'] = False 
            data['form_errors'] = str(form.errors)  
    else:
        form = RequestForm(instance=temp_request_from_helpdesk, initial={'tasks': literal_eval(temp_request_from_helpdesk.tasks)})
        context = {'form': form}
        data['html_form'] = render_to_string('modal_create_form.html', context, request=request)
    return JsonResponse(data)   

@login_required
def request_edit(request, request_id):
    data = dict()       
    request_from_helpdesk = get_object_or_404(Request, number=request_id)
    if request.method == 'POST':
        if not is_superuser(request.user):
            form = WorkerRequestForm(request.POST, instance=request_from_helpdesk)
        else:
            form = RequestForm(request.POST, instance=request_from_helpdesk)        
        if form.is_valid():
            form.save()
            requests = Request.objects.order_by('-number')
            context = paginate (requests, request)
            data['form_is_valid'] = True
            data['html_book_list'] = render_to_string('requests_list.html', context)    
        else:
            data['form_is_valid'] = False 
            data['form_errors'] = str(form.errors)
            print (form.errors)
    else:
        tasks = RequestTasks.objects.filter(request=request_id).values_list('tasklist', flat=True)
        if not is_superuser(request.user):
            form = WorkerRequestForm(instance=request_from_helpdesk, initial={'tasks': list(tasks)})
            print ('worker')
        else:
            form = RequestForm(instance=request_from_helpdesk, initial={'tasks': list(tasks)})
        context = {'form': form}
        data['html_form'] = render_to_string('modal_edit_form.html', context, request=request)
    return JsonResponse(data)   

@login_required
@user_passes_test(is_superuser)
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
        else:
            print(form.errors)
    return render(request, 'index.html', {'form': form})