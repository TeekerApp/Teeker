from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

import os
import requests

# Get custom models
from .models import feedback_content, account_settings

# Used to store password recovery urls
recovery_url_email = {}
recovery_email_url = {}
recovery_urls = []

# Create your views here.

def index(request, search=None):
    """Used for Home page"""

    if not search:
        search="oyrq-qzOx1U" # If no searches have been made use this as default

    url = f'https://www.googleapis.com/youtube/v3/videos?id={search}&key={settings.GOOGLE_API}&part=status'
    url_get = requests.get(url)
    try:
        if url_get.json()["items"][0]["status"]["publicStatsViewable"]:
            print("Video is publicly available")
    except:
        search="oyrq-qzOx1U"
        print("Video does not exist.")

    html_content = {"message": "G",
                    "title": "My Morning Vibes",
                    "average_rating": 8,
                    "youtube_easteregg": search}

    if request.user.is_staff:
        return render(request, "TeekerApp/index.html", html_content)
    else:
        return render(request, "TeekerApp/not_staff.html", html_content)


def search_bar(request): # For now this is just used as a Alpha Easter Egg
    """ Displays the profile of other users in a different way compared to when you own the account. """

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html")

    if request.method == "POST":

        if request.POST["search"]:
            yt_video = str(request.POST["search"])
        else:
            print("Nothing to search...")

    return HttpResponseRedirect(reverse("index_search", args=(yt_video,)))


def get_client_ip(request):
    """ Used in register for reCAPTCHA verification. This gets the users Public IP address """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def register(request):
    """Used for sign up/register page"""

    # Make sure the user is sent to the home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

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
        try:
            request.POST["custom_U1133"]
        except KeyError:
            return render(request, "TeekerApp/register.html", {"message": "You didn't agree to the Terms And Conditions!"})

        # Check if the reCAPTCHA was successful (reCAPTCHA v2.0)
        try:
            if not request.POST["g-recaptcha-response"]:
                return render(request, "TeekerApp/register.html", {"message": "Failed to check reCAPTCHA."})
            else:
                captcha_rs = request.POST["g-recaptcha-response"]
                url = "https://www.google.com/recaptcha/api/siteverify"
                params = {
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": captcha_rs,
                    "remoteip": get_client_ip(request),
                    "success": True|False,
                    "hostname": settings.ALLOWED_HOSTS
                }
                verify_rs = requests.get(url, params=params, verify=True)
                verify_rs = verify_rs.json()
                if not verify_rs["success"]:
                    return render(request, "TeekerApp/register.html", {"message": "reCAPTCHA not valid. Try again in 1 minute."})
        except KeyError:
            return render(request, "TeekerApp/register.html", {"message": "Failed to check reCAPTCHA."})

        # Check if the Password matches the requirements
        if len(password) > 7 and len(password) < 65:
            if password != passwordconfirm:
                return render(request, "TeekerApp/register.html", {"message": "Passwords don't match!"})
        else:
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
            return render(request, "TeekerApp/register.html", {"message": "username exists! Please use another one."})

        # Check if the email already exists in the Database
        try:
            User.objects.get(email=e_mail)
            result["EMAIL_CHECK"] = True
        except User.DoesNotExist:
            result["EMAIL_CHECK"] = False
        
        # If the username does exist send a message
        if result["EMAIL_CHECK"]:
            return render(request, "TeekerApp/register.html", {"message": "email exists! Please use another one."})
        
        # If the credentials are valid register the user to the Database
        if not result["EMAIL_CHECK"] and not result["USERNAME_CHECK"]:
            f = User.objects.create_user(username=username,
                                        email=e_mail,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password)
            f.save() # Save the new users details to the Database

            account_settings(owner=int(request.user.pk),
                            news_letter=False # For now the News letter option will stay Disabled till futher notice
                            ).save()
            
            # Send the new user a email
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


def register_validation(request, option):
    """ Used by the Register page Javascript to check if the user has valid credidentionals """

    # Check if the username already exists in the Database
    if option == "username":
        username = str(request.POST["username"])
        try:
            User.objects.get(username=username)
            return JsonResponse({"STATUS": False})
        except User.DoesNotExist:
            return JsonResponse({"STATUS": True})
    
    # Check if the email address already exists in the Datavase
    elif option == "email":
        email = str(request.POST["email"])
        try:
            User.objects.get(email=email)
            return JsonResponse({"STATUS": False})
        except User.DoesNotExist:
            return JsonResponse({"STATUS": True})

    return JsonResponse({"STATUS": True})


def login_page(request):
    """ Used for Login Page """

    # Check if the user if still logged in or not
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        # Get the credentials from the input fields
        username = str(request.POST["username"])
        pwd = str(request.POST["pwd"])

        # Check if the credentials are valid
        user = authenticate(request, username=username, password=pwd)

        # Log the user in if the credentials are valied
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


def forgot_pwd(request, html_content=None):
    """ Used for recovering user password """

    # Make sure the user is sent to the home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        # Check if the email the user gave exists in the Database
        email = str(request.POST["email"])
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            html_content = {
                "option": "email",
                "message": "User with that email address does not exist."
            }
            return render(request, "TeekerApp/forgot_pwd.html", html_content)

        # Store the users credentials in f
        f = User.objects.get(email=email)
        while True:

            # Get a random string to make the random URL
            r_url = str(get_random_string(length=32))

            # Check if the string doesn't exist in the URL list
            if r_url not in recovery_urls:

                # Check if the email address is already waiting
                try:
                    if recovery_email_url[email]:

                        html_content = {
                            "option": "email",
                            "message": "Email already sent. If you haven't recieved the email please contact Support. ERx2"
                        }
                        return render(request, "TeekerApp/forgot_pwd.html", html_content)
                except KeyError:
                    recovery_urls.append(r_url) # Place the random string URL in the list
                    recovery_email_url[email] = r_url # Place the random string URL in the dictionary with the key being the email address
                    recovery_url_email[r_url] = email # Place the email address in the dictionary with the key being the random string URL

                    # Send the random string URL to the email address provided by the user
                    send_mail("Forgot Password",
                            """Forgot Your password?
                            Use this link: """+str(request.META["HTTP_HOST"])+"/forgot_pwd/"+r_url,
                            os.getenv("EMAIL"),
                            [f.email],
                            fail_silently=False,
                            html_message="""<h3>Forgot Your Password?</h3>
                                            <p>Use this Link to recover your account:</p>"""+str(request.META["HTTP_HOST"])+"/forgot_pwd/"+r_url+"""
                                            <br>
                                            <small class='text text-muted'>Don't reply to this email.</small>""")
                    break # Break the loop
        html_content = {
                "option": "email",
                "success_message": "Check your inbox now. (If you can't find it check the spam mail)"
            }
        return render(request, "TeekerApp/forgot_pwd.html", html_content)

    elif request.method == "GET":
        if not html_content:
            html_content = {
                "option": "email",
                "message": ""
            }

    return render(request, "TeekerApp/forgot_pwd.html", html_content)


def forgot_pwd_handler(request, option):
    """ Used to handle the forgot password URL and password changes """

    # Make sure the user is sent to the home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # Check if the URL in the option variable doesn't exists in the 'recovery_urls' list
    if option not in recovery_urls:
        return HttpResponseRedirect(reverse("forgot_pwd")) # Redirect user to the page where they have to put the email address

    html_content = {
        "option": "pwd",
        "url": option
    }

    return render(request, "TeekerApp/forgot_pwd_2.html", html_content)


def forgot_pwd_change(request, option):
    """ Used to update the account password to the new one. """

    # Make sure the user is sent to the home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        # Collect all data from input fields
        url = str(request.POST["ust_url"])
        pwd = str(request.POST["pwd"])
        cpwd = str(request.POST["cpwd"])

        # Check if the reCAPTCHA was successful (reCAPTCHA v2.0)
        try:
            if not request.POST["g-recaptcha-response"]:
                html_content = {
                    "option": "email",
                    "message": "Failed to check reCAPTCHA."
                }
                return render(request, "TeekerApp/forgot_pwd.html", html_content)
            else:
                captcha_rs = request.POST["g-recaptcha-response"]
                url_recaptcha = "https://www.google.com/recaptcha/api/siteverify"
                params = {
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": captcha_rs,
                    "remoteip": get_client_ip(request)
                }
                verify_rs = requests.get(url_recaptcha, params=params, verify=True)
                verify_rs = verify_rs.json()
                if not verify_rs["success"]:
                    html_content = {
                        "option": "email",
                        "message": "reCAPTCHA not valid. Try again in 1 minute."
                    }
                    return render(request, "TeekerApp/forgot_pwd.html", html_content)
        except KeyError:
            html_content = {
                "option": "email",
                "message": "Failed to check reCAPTCHA."
            }
            return render(request, "TeekerApp/forgot_pwd.html", html_content)

        # Check if the new password meets requirements
        if len(pwd) > 7 or len(pwd) < 65 and len(cpwd) > 7 or len(cpwd) < 65:

            # Check if the new password and confirm password match
            if pwd == cpwd:
                
                if url in recovery_urls:
                    email = recovery_url_email[url] # Get the email address related to the url key
                    
                    # Update the users password
                    f = User.objects.get(email=email)
                    f.set_password(pwd)
                    f.save()

                    # Remove the URL and email address from the list and dictionary
                    try:
                        recovery_urls.remove(url)
                        del recovery_email_url[email]
                        del recovery_url_email[url]
                    except KeyError:
                        print("Failed to remove URL and Email address from Recovery Password.")

                    return HttpResponseRedirect(reverse("index")) # Send user to home page
                else:
                    html_content = {
                        "option": "email",
                        "message": "URL broken!"
                    }
                    return render(request, "TeekerApp/forgot_pwd.html", html_content)
            else:
                html_content = {
                    "option": "email",
                    "message": "The passwords don't match!"
                }
                return render(request, "TeekerApp/forgot_pwd.html", html_content)
        else:
            html_content = {
                "option": "email",
                "message": "Your new password does not meet our requirements."
            }
            return render(request, "TeekerApp/forgot_pwd.html", html_content)
    else:
        html_content = {
            "option": "email",
            "message": "Something went wrong."
        }
        return render(request, "TeekerApp/forgot_pwd.html", html_content)

    return HttpResponseRedirect(reverse("forgot_pwd"))
    

def account(request):
    """ Used for account page to display Account information """
    
    html_content = {"":""}

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html", html_content)
    
    return render(request, "TeekerApp/account.html", html_content)


def feedback(request):
    """ Used for giving feedback. Mostly looking for bug issue reports. """

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html")

    if request.method == "POST":

        if request.POST["subject"]:
            subject_v = str(request.POST["subject"])

            if request.POST["message"]:
                message_v = str(request.POST["message"])

                # Check if the reCAPTCHA was successful (reCAPTCHA v2.0)
                try:
                    if not request.POST["g-recaptcha-response"]:
                        html_content = {"alert_message": "Failed to check reCAPTCHA."}
                    else:
                        captcha_rs = request.POST["g-recaptcha-response"]
                        url_recaptcha = "https://www.google.com/recaptcha/api/siteverify"
                        params = {
                            "secret": settings.RECAPTCHA_SECRET_KEY,
                            "response": captcha_rs,
                            "remoteip": get_client_ip(request)
                        }
                        verify_rs = requests.get(url_recaptcha, params=params, verify=True)
                        verify_rs = verify_rs.json()
                        if not verify_rs["success"]:
                            html_content = {"alert_message": "reCAPTCHA not valid. Try again in 1 minute."}
                except KeyError:
                    html_content = {"alert_message": "Failed to check reCAPTCHA."}

                feedback_content(owner=int(request.user.pk),
                                 subject=subject_v,
                                 feedback=message_v).save()
                
                # Get all FeedBack Data
                p_feedback = feedback_content.objects.all()
                if p_feedback:
                    feedback_html_c = []
                    for i in p_feedback:
                        p_user = User.objects.get(pk=int(i.owner))
                        feedback_html_c.append({
                            "username": p_user.username,
                            "subject": i.subject,
                            "feedback_message": i.feedback,
                            "date": i.date
                            })

                    html_content = {
                        "feedback_html": feedback_html_c,
                        "success_message": "FeedBack has been Received and will be viewed soon! Thank You."
                        }
                else:
                    html_content = {"success_message": "FeedBack has been Received and will be viewed soon! Thank You."}

                return render(request, "TeekerApp/feedback.html", html_content)
            else:
                html_content = {"alert_message": "FeedBack Message missing!"}
                return render(request, "TeekerApp/feedback.html", html_content)
        else:
            html_content = {"alert_message": "Subject is missing!"}
            return render(request, "TeekerApp/feedback.html", html_content)

    elif request.method == "GET":

        # Get all FeedBack Data
        p_feedback = feedback_content.objects.all()
        if p_feedback:
            feedback_html_c = []
            for i in p_feedback:
                p_user = User.objects.get(pk=int(i.owner))
                feedback_html_c.append({
                    "username": p_user.username,
                    "subject": i.subject,
                    "feedback_message": i.feedback,
                    "date": i.date
                    })

            html_content = {
                "feedback_html": feedback_html_c
                }
        else:
            html_content = {"":""}

    return render(request, "TeekerApp/feedback.html", html_content)


def settings_page(request):
    """ Used to show the users account settings and allow them to modify them. """

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html")

    try:
        f = account_settings.objects.get(owner=int(request.user.pk))
        if f:
            html_content = {
                "news_letter": f.news_letter,
                "inbox_notifications": f.inbox_notifications,
                "browser_notifications": f.browser_notifications
            }
    except account_settings.DoesNotExist:
        html_content = {
            "news_letter": False,
            "inbox_notifications": False,
            "browser_notifications": False
        }

        # I don't know if this should be here or not (This might be removed in the future)
        account_settings(owner=int(request.user.pk),
                            news_letter=False # For now the News letter option will stay Disabled till futher notice
                            ).save()

    return render(request, "TeekerApp/settings.html", html_content)


def inbox(request):
    """ Shows the messages the user has recieved from other users. A little communication page. """

    html_content = {"":""}

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html", html_content)

    return render(request, "TeekerApp/inbox.html", html_content)


def subscriptions(request):
    """ Shows the content of the user's the user is following. """

    html_content = {"":""}

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html", html_content)

    return render(request, "TeekerApp/subscriptions.html", html_content)


def upload_post(request):
    """ Used to upload the users content to our database and server. """

    html_content = {"":""}

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html", html_content)

    return render(request, "TeekerApp/upload_post.html", html_content)


def visitor_account_view(request):
    """ Displays the profile of other users in a different way compared to when you own the account. """

    html_content = {"":""}

    # Check if the user is Staff (Only Staff are allowed to view this page)
    if not request.user.is_staff:
        return render(request, "TeekerApp/not_staff.html", html_content)

    return render(request, "TeekerApp/visitor_account_view.html", html_content)

    