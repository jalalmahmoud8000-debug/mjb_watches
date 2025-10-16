from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import RegisterForm, ProfileForm
from orders.models import Order


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			login(request, user)
			return redirect('home')
	else:
		form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})


def profile(request):
	if not request.user.is_authenticated:
		return redirect('accounts:login')
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('accounts:profile')
	else:
		form = ProfileForm(instance=request.user)
	return render(request, 'accounts/profile.html', {'form': form})


def order_history(request):
	if not request.user.is_authenticated:
		return redirect('accounts:login')
	orders = Order.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'accounts/orders.html', {'orders': orders})


# Create your views here.


def logout_view(request):
	# allow GET logout for convenience from navbar
	logout(request)
	return redirect('home')
