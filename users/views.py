from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index:index'))

def register_view(request):

#    if request.user.is_authenticated:
#        return HttpResponseRedirect(reverse('study_session:overview'))

    if request.method != 'POST':
        form = UserCreationForm()

    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():

            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username,
            password=request.POST['password1'])
            login(request, authenticated_user)

            return HttpResponseRedirect(reverse('index:index'))

    context = {'form': form }
    return render(request, 'users/register.html', context)
