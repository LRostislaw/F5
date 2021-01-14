from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from .forms import ADForm
from .models import AD


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "main/signup.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "main/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class ChangeFormView(UpdateView):
    form_class = PasswordChangeForm
    template_name = 'main/edit_password.html'
    success_url = 'main/settings.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(ChangeFormView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs


def index(request):
    return render(request, 'main/index.html')


def statistic(request):
    if request.method == 'POST':
        form = ADForm(request.POST)
        if form.is_valid():
            listener = form.save(commit=False)
            listener.user = request.user
            listener.save()
            return redirect('/statistic')
    form = ADForm()
    user_name = request.user
    statistics = AD.objects.order_by('time').filter(user=user_name)[:20]
    data = {
        'form': form,
        'statistics': statistics
    }
    return render(request, 'main/statistic.html', data)


def settings(request):
    return render(request, 'main/settings.html')