# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from userprofiles.utils import get_form_class
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

class RegistrationView(FormView):
    form_class = get_form_class('userprofiles.forms.RegistrationForm')
    template_name = 'userprofiles/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # return redirect(up_settings.REGISTRATION_REDIRECT)
        url = reverse('users:userprofiles_registration_complete')
        return HttpResponseRedirect(url)

registration = RegistrationView.as_view()

class RegistrationCompleteView(TemplateView):
    template_name = 'userprofiles/registration_complete.html'

    def get_context_data(self, **kwargs):
        return {
            'account_verification_active': False,
            'expiration_days': 7,
        }
registration_complete = RegistrationCompleteView.as_view()

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/blog/')
            else:
                return HttpResponse("Your Blog account is disabled.")
        else:

            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'blog/index.html', {})
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
