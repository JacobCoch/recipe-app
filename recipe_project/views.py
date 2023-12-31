from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.conf import settings
from .forms import LoginForm, SignUpForm


def success(request):
    logout(request)  # the use pre-defined Django function to logout
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "auth/success.html", context)


# define a function view called login_view that takes a request from user
def login_view(request):
    error_message = None
    success_message = None
    form = LoginForm()  # Use the CustomLoginForm

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                success_message = "You have successfully logged in!"
                return redirect("recipes:home")
            else:
                error_message = "Oops, something went wrong."

    context = {
        "form": form,
        "error_message": error_message,
        "success_message": success_message,
        'MEDIA_URL': settings.MEDIA_URL,

    }
    return render(request, "auth/login.html", context)


def signup(request):
    error_message = None
    success_message = None
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            # Create the user and log them in
            user = form.create_user()

            login(request, user)
            success_message = "You have successfully signed up!"
            return redirect("recipes:home")

        else:
            error_message = "Oops, something went wrong during signup."
                
    context = {
        "form": form,
        "error_message": error_message,
        "success_message": success_message,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    
    return render(request, "auth/signup.html", context)
