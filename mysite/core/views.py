from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import pyttsx3

# Create your views here.
def home(request):
	count = User.objects.count()
	return render(request, 'home.html', {
		'count': count
		})


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'form': form
		})

def get_cmd(request):
	if request.GET.get('cmd'):
		cmd = request.GET.get('cmd')
		result = request.GET.get('cmd')
		# now do your work here and return the result to play.html
		return render(request, 'play.html', {'result':result})

@login_required
def secret_page(request):
	return render(request, 'secret_page.html')

@login_required
def play(request):
	engine = pyttsx3.init()
	engine.say("You Just Started the flow")
	engine.runAndWait()
	return render(request, 'play.html')

def how_work(request):
	return render(request, 'how_work.html')
