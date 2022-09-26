# Internal imports
from .models import Observation, PestTrap
from .serializers import PestTrapSerializer, UserSerializer
from .forms import ObservationForm, PestTrapForm

# AuthN and AuthZ
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Misc imports
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response


# Simple pass/fail authz check for pest trap and observation table access
def is_inspector(user):
    check = user.groups.filter(name="inspectors").exists() or \
        user.groups.filter(name="growers").exists()
    return check


# Render the front page
class IndexView(TemplateView):
    template_name = "core/index.html"

######################
##### PEST TRAPS #####
######################

@login_required(login_url="/accounts/login/")
def pest_trap_registration(request):
    if not is_inspector(request.user):
        raise PermissionDenied

    # If the user is sending the form (not loading it)
    if request.method == "POST":

        # Instatiate the form based on the PestTrapForm model
        form = PestTrapForm(request.POST)

        # Check the form's valid (no nulls; no errors)
        if form.is_valid():

            # 1. Process the 'cleaned data'...
            id = form.cleaned_data["id"]
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            trap = PestTrap(id=id, name=name, description=description)

            # 2. Save the form data to the DB
            trap.save()

            # 3. Redirect to the pest trap table
            return HttpResponseRedirect("/pest-trap-table/")

    else:  # The user is loading the form the first time.
        form = PestTrapForm()

    return render(request, "pest_trap_registration.html", {"form": form})


# Tabular display of all registered pest traps
@login_required(login_url="/accounts/login/")
def pest_trap_table(request):
    if not is_inspector(request.user):
        raise PermissionDenied
    query_results = PestTrap.objects.all()
    return render(request, "pest_trap_table.html", {"query_results": query_results})

# Display of individual trap record
@login_required(login_url="/accounts/login/")
def pest_trap_record(request, id):
    trap = PestTrap.objects.filter(id=id)
    observations = Observation.objects.filter(pestTrap=id)
    context = {
        "id": id,
        "trap": trap,
        "observations": observations
    }
    return render(request, 'pest_trap_record.html', context)

######################
#### OBSERVATIONS ####
######################

@login_required(login_url="/accounts/login/")
def observation_registration(request):
    if not is_inspector(request.user):
        raise PermissionDenied
    # If the user is sending the form (not loading it)
    if request.method == "POST":

        # Instatiate the form based on the PestTrapForm model
        form = ObservationForm(request.POST)

        # Check the form's valid (no nulls; no errors)
        if form.is_valid():

            # 1. Process the 'cleaned data'...
            id = form.cleaned_data["id"]
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            pestTrap = form.cleaned_data["pestTrap"]
            observation = Observation(
                id=id,
                name=name,
                description=description,
                pestTrap=pestTrap,
            )

            # 2. Save the form data to the DB
            observation.save()

            # 3. Redirect to the form submission page
            return HttpResponseRedirect("/observation-table/")

    else:  # The user is loading the form the first time.
        form = ObservationForm()

    return render(request, "observation_registration.html", {"form": form})


# Tabular display of all pest trap observations
@login_required(login_url="/accounts/login/")
def observation_table(request):
    if not is_inspector(request.user):
        raise PermissionDenied
    query_results = Observation.objects.all()
    return render(request, "observation_table.html", {"query_results": query_results})


######################
######## USER ########
######################

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/pest-trap-table/")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})




# class UserViewSet2(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_object(self):
#         pk = self.kwargs.get("pk")

#         if pk == "current":
#             return self.request.user

#         return super().get_object()

#     def get_queryset(self):
#         req = self.request
#         if req:
#             self.queryset = User.objects.filter(id=req.user.id)
#             print("request accessed")
#             return self.queryset
#         else:
#             print("request not accessed")
#             return self.queryset


# class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     serializer_class = UserSerializer
#     # queryset = User.objects.filter(user=self.request.user)

#     def get_object(self):
#         return self.request.user


# class PestTrapViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Pest Traps to be viewed or editted.
#     """

#     queryset = PestTrap.objects.all()
#     serializer_class = PestTrapSerializer

#     def update(self, request, pk=None, *args, **kwargs):
#         user = request.user
#         instance = self.get_object()
#         print(" user ", instance.users)
#         print(" user ", user.id)
#         print(" data ", request.data)
#         instance.users.add(user)  # doesn't appear to work
#         instance.save()
#         print(" modified instance ", instance.users)

#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(serializer.data)

