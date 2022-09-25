from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import viewsets, status, mixins
from .models import Observation, PestTrap
from .serializers import PestTrapSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Django tutorial
# https://docs.djangoproject.com/en/4.1/topics/forms/
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ObservationForm, PestTrapForm

# Create your views here.
class IndexView(TemplateView):
    template_name = "core/index.html"


# Logic for processing new trap registrations
def PestTrapFormView(request):

    # If the user is sending the form (not loading it)
    if request.method == "POST":

        # Instatiate the form based on the PestTrapForm model
        form = PestTrapForm(request.POST)

        # Check the form's valid (no nulls; no errors)
        if form.is_valid():

            # 1. Process the 'cleaned data'...
            name = form.cleaned_data["name"]
            UniqueId = form.cleaned_data["UniqueId"]
            description = form.cleaned_data["description"]
            trap = PestTrap(
                name=name, UniqueId=UniqueId, description=f"modified {description}"
            )

            # 2. Save the form data to the DB
            trap.save()

            # 3. Redirect to the form submission page
            return HttpResponseRedirect("/pest-trap-form/")

    else:  # The user is loading the form the first time.
        form = PestTrapForm()

    return render(request, "pest_trap_form.html", {"form": form})


def ObservationFormView(request):

    # If the user is sending the form (not loading it)
    if request.method == "POST":

        # Instatiate the form based on the PestTrapForm model
        form = ObservationForm(request.POST)

        # Check the form's valid (no nulls; no errors)
        if form.is_valid():

            # 1. Process the 'cleaned data'...
            name = form.cleaned_data["name"]
            UniqueId = form.cleaned_data["UniqueId"]
            description = form.cleaned_data["description"]
            pestTrap = form.cleaned_data["pestTrap"]
            observation = Observation(
                name=name,
                UniqueId=UniqueId,
                description=f"modified {description}",
                pestTrap=pestTrap,
            )

            # 2. Save the form data to the DB
            observation.save()

            # 3. Redirect to the form submission page
            return HttpResponseRedirect("/observation-form/")

    else:  # The user is loading the form the first time.
        form = ObservationForm()

    return render(request, "observation_form.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/app/")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


class UserViewSet2(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")

        if pk == "current":
            return self.request.user

        return super().get_object()

    def get_queryset(self):
        req = self.request
        if req:
            self.queryset = User.objects.filter(id=req.user.id)
            print("request accessed")
            return self.queryset
        else:
            print("request not accessed")
            return self.queryset


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    # queryset = User.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user


class PestTrapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Pest Traps to be viewed or editted.
    """

    queryset = PestTrap.objects.all()
    serializer_class = PestTrapSerializer

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        print(" user ", instance.users)
        print(" user ", user.id)
        print(" data ", request.data)
        instance.users.add(user)  # doesn't appear to work
        instance.save()
        print(" modified instance ", instance.users)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
