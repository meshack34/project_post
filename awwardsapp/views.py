from django.shortcuts import render
from collections import UserString
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from awwardsapp.models import Profile,Project,Rating
from .forms import ProfileForm,NewProjectForm
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Project
from .serializer import ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly





# Create your views here.
# @login_required(login_url='/accounts/login/')
def index(request):
    project = Project.objects.all().order_by('-id')

    return render(request, 'main/index.html',{'projects':project})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    project = Project.objects.filter(user_id=current_user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/profile.html', {"form":form,'projects':project,'profile':profile})
@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('index')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        images = Project.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'main/search.html', {'message': message, 'images': images})
    else:
        message = 'Not found'
    return render(request, 'main/search.html', {'message': message})


    #Rate view function
@login_required(login_url='/accounts/login/')
def rate(request,id):
    if request.method == 'POST':
        project = Project.objects.get(id = id)
        current_user = request.user
        design_rate = request.POST['design']
        content_rate = request.POST['content']
        usability_rate = request.POST['usability']
        Rating.objects.create(project=project,user=current_user,design_rate=design_rate,usability_rate=usability_rate,content_rate=content_rate,average=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),)

        return render(request,"main/project_review.html",{"project":project})
    else:
        project = Project.objects.get(id = id) 
        return render(request,"main/project.html",{"project":project})

@login_required(login_url='/accounts/login/')
def project_review(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = Rating.objects.filter(project = project)
    return render(request, "main/project_review.html", {"project": project, 'rating':rating})

class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
