from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.core.cache import cache


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			#ct = cache.get('count', version=user.pk)
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			#user.login_count = ct
			if user:
				login(request, user)
				#return render(request, "home", {'email':email, 'password':password, 'login_count':user.login_count})
				return redirect("home")

	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
			return redirect("home")
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
					"employee_id": request.user.employee_id,
					"login_count": request.user.login_count,
				}
			)


	context['account_form'] = form
	if request.user.is_admin:
		return render(request, "account/account_admin.html", context)
	if request.user.is_active:
		return render(request, "account/account_active.html", context)
	else:
		return render(request, "account/account.html", context)

