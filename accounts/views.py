from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["password2"]:
                messages.error(request, "Passwords do not match")
                return redirect("signup")
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(request, "Username already taken")
                return redirect("signup")
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home.index")  # change to your homepage
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home.index")
