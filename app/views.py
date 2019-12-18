from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

import os

# Create your views here.

def index(request):
    """Used for Home page"""
    html_content = {"message": "G"}
    return render(request, "TeekerApp/index.html", html_content)

def register(request):
    """Used for sign up/register page"""

    # Check if the request is POST
    if request.method == "POST":

        # Get the credentials to use to register the user
        username = str(request.POST["username"])
        first_name = str(request.POST["first_name"])
        last_name = str(request.POST["last_name"])
        e_mail = str(request.POST["email"])
        password = str(request.POST["pwd"])
        passwordconfirm = str(request.POST["cpwd"])
		
        # Used later for phone number authentication to prevent spam accounts
        # The code to save this to the Database will need to be written later
        #phonenumber = str(request.POST["phonenumber"])

        # Check if the check box was ticket that says that the user agrees with the Terms and Conditions
        if not request.POST["check_box"]:
            print("You didn't agree to the Terms And Conditions!")
            return render(request, "TeekerApp/register.html", {"message": "You didn't agree to the Terms And Conditions!"})

        # Check if the Password matches the requirements
        if len(password) > 7 and len(password) < 65:
            if password != passwordconfirm:
                print("Passwords don't match")
                return render(request, "TeekerApp/register.html", {"message": "Passwords don't match!"})
        else:
            print("Password too short! Please make it longer then 8 characters and less the 64.")
            return render(request, "TeekerApp/register.html", {"message": "Password too short! Please make it longer then 8 characters and less the 64."})

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
            return render(request, "TeekerApp/register.html", {"message": "username exists! Please use another one."})

        # Check if the email already exists in the Database
        try:
            User.objects.get(email=e_mail)
            result["EMAIL_CHECK"] = True
        except User.DoesNotExist:
            result["EMAIL_CHECK"] = False
        
        # If the username does exist send a message
        if result["EMAIL_CHECK"]:
            print("email exists! Please use another one.")
            return render(request, "TeekerApp/register.html", {"message": "email exists! Please use another one."})
        
        # If the credentials are valid register the user to the Database
        if not result["EMAIL_CHECK"] and not result["USERNAME_CHECK"]:
            f = User.objects.create_user(username=username,
                                        email=e_mail,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password)
            f.save()
            print("Success you were registered!")

            send_mail("Welcome To Teeker",
                        """Welcome to Teeker. 
                            Thank You For Joining our Community, we hope you have fun. 
                            Don't reply to this email.""",
                        os.getenv("EMAIL"),
                        [e_mail],
                        fail_silently=False,
                        html_message="""<h2>Welcome To Teeker</h2>
                                        <br>
                                        Thank You For Joining our Community, have FUN!
                                        <br>
                                        <br>
                                        <small class='text text-muted'>Don't reply to this email.</small>""")
        return HttpResponseRedirect(reverse("index"))

    return render(request, "TeekerApp/register.html")


def login_page(request):
    """ Used for Login Page """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        print("POST on Login")

        username = str(request.POST["username"])
        pwd = str(request.POST["pwd"])

        user = authenticate(request, username=username, password=pwd)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "TeekerApp/login.html", {"message": "Invalid username/email or password!"})

    return render(request, "TeekerApp/login.html")
	
def logout_page(request):
    """ Used for logging out the user """
    
    logout(request) # Log out the user from the server
    
    return HttpResponseRedirect(reverse("login"))
    

def account(request):
    """ Used for account page to display Account information """
    
    html_content = {""}
    
    return render(request, "TeekerApp/account.html", html_content)
    