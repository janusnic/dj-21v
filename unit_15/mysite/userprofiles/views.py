# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.views.generic import FormView, RedirectView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from userprofiles.utils import get_form_class
from .models import UserProfile
from .forms import UserProfileForm

from django.core.urlresolvers import reverse_lazy

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    form_class = AuthenticationForm
    template_name = "userprofiles/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME


    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    #def get_success_url(self):
    #    redirect_to = self.request.GET.get(self.redirect_field_name)
    #    if not is_safe_url(url=redirect_to, host=self.request.get_host()):
    #        redirect_to = self.success_url
    #    return redirect_to

    def get_success_url(self):
        return reverse("users:profile", kwargs={"slug": self.request.user})


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

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


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = 'userprofiles/user_detail.html'

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

profile = UserProfileDetailView.as_view()

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "userprofiles/edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("users:profile", kwargs={"slug": self.request.user})
