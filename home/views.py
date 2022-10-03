from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q



# Create your views here.
def index(request):
    return render(request,'index.html')



      # Adding the New User 

def handleSignup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        # Checking the inputs are valid




        # Creating the user

        MyUser = User.objects.create_user(username,email,password)
        MyUser.save()
        messages.success(request,"Your account has been created Successfully")
        return redirect('/')
    
    return render(request,'signup.html')



def loginUser(request):
    if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            # check if user has entered correct credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/services")

            else:
                # No backend authenticated the credentials
                return render(request, 'login.html')

    return render(request, 'login.html')
    



    

def logoutuser(request):
    logout(request)
    return redirect("/login")

def services(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request,'Info Sent Successfully')

    return render(request,'contact.html')

# Reset the Password

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Django',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid data found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



        





