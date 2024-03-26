from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Estudiante, Taller


def home(request):
	Estudiantes = Estudiante.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'Estudiante':Estudiantes})


def estudiantes_por_taller(request, taller_id):
    taller = Taller.objects.get(nombre=taller_id)
    estudiantes = Estudiante.objects.filter(taller=taller)
    return render(request, 'home.html', {'taller': taller, 'Estudiante': estudiantes})


def search(request):
    query = request.GET.get('query')
    estudiantes = Estudiante.objects.filter(nombre__icontains=query)
    return render(request, 'home.html', {'estudiantes': estudiantes, 'query': query})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		Estudiantes = Estudiante.objects.get(id=pk)
		return render(request, 'record.html', {'Estudiante':Estudiantes})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Estudiante.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        else:
            form = AddRecordForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')



def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Estudiante.objects.get(id=pk)
        if request.method == "POST":
            form = AddRecordForm(request.POST, request.FILES, instance=current_record)
            if form.is_valid():
                form.save() 
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')
        else:
            form = AddRecordForm(instance=current_record)
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

