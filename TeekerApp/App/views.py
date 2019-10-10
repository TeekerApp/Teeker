from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    """Used for Home page"""
	
    return render(request, "TeekerApp/index.html", html_content)

def register(request):
    """Used for sign up/register page"""

    # Check if the request is POST
    if request.method == "POST":

        # Get the credentials to use to register the user
        username = str(request.POST["username"])
        first_name = str(request.POST["first_name"])
        last_name = str(request.POST["last_name"])
        e_mail = str(request.POST["e_mail"])
        password = str(request.POST["password"])
        passwordconfirm = str(request.POST["passwordconfirm"])
		
        # Used later for phone number authentication to prevent spam accounts
        # The code to save this to the Database will need to be written later
        #phonenumber = str(request.POST["phonenumber"])

        print(username)
        print(first_name)
        print(last_name)
        print(e_mail)

        if password != passwordconfirm:
            print("Passwords don't match")
            return render(request, "TeekerApp/register", {"message": "Passwords don't match!")

        # Iniatialize variable
        result = {}

        # Check if the username already exists in the Database
        try:
            User.objects.get(username=username)
            result["USERNAME_CHECK"] = True
        except User.DoesNotExist:
            result["USERNAME_CHECK"] = False

        # If the username does exist send a message
        if result["USERNAME_CHECK"]:
            print("username exists! Please use another one.")
            return render(request, "TeekerApp/register", {"message": "username exists! Please use another one.")

        # Check if the email already exists in the Database
        try:
            User.objects.get(email=e_mail)
            result["EMAIL_CHECK"] = True
        except User.DoesNotExist:
            result["EMAIL_CHECK"] = False
        
        # If the username does exist send a message
        if result["EMAIL_CHECK"]:
            print("email exists! Please use another one.")
            return render(request, "TeekerApp/register", {"message": "email exists! Please use another one.")
        
        # If the credentials are valid register the user to the Database
        if not result["EMAIL_CHECK"] and not result["USERNAME_CHECK"]:
            f = User.objects.create_user(username=username,
                                        email=e_mail,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password)
            f.save()
            print("Success you were registered!")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "TeekerApp/register")	