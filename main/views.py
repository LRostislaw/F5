from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout, authenticate
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from .forms import ADForm, TypeForm, ChangeUserInfoForm
from .models import AD, TypeData


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login"
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
        if 'add_data' in request.POST:
            form = ADForm(request.POST)
            if form.is_valid():
                listener = form.save(commit=False)
                listener.user = request.user
                listener.type = TypeData.objects.get(id=request.POST.get("add_data"))
                listener.save()
                return redirect('/statistic')
        if 'add_type' in request.POST:
            form = TypeForm(request.POST)
            if form.is_valid():
                listener = form.save(commit=False)
                listener.user = request.user
                listener.label = dict(form.choices)[form.cleaned_data["label"]]
                listener.save()
                return redirect('/statistic')

    FormAD = ADForm()
    user_name = request.user
    types = TypeData.objects.order_by('-id').filter(user=user_name)
    FormType = TypeForm()
    statistics = AD.objects.order_by('time').filter(user=user_name)
    data = {
        'FormAD': FormAD,
        'FormType': FormType,
        'statistics': statistics,
        'type': types
    }
    return render(request, 'main/statistic.html', data)


class Settings(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/settings.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('settings')
    success_message = 'Изменения сохранены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def privacy(request):
    return render(request, 'main/privacy.html')
