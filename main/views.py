from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from .forms import ADForm, TypeForm, ChangeUserInfoForm, RegisterUserForm, AddPatientForm
from .models import AD, TypeData, puser
from .utilities import signer, send_choice_notification


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(puser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)


def choice_doctor(request, sign, email):
    user = puser.objects.get(email=email)
    doctor = puser.objects.get(username=sign)
    if user.is_doctor:
        template = 'bad_signature_choice.html'
    else:
        if user.user == doctor:
            template = 'main/doctor_is_choice.html'
        else:
            template = 'main/choice_done.html'
            user.user = doctor
            user.save()
    return render(request, template)


class RegisterFormView(CreateView):
    model = puser
    success_url = reverse_lazy('signup_done')
    form_class = RegisterUserForm
    template_name = "main/signup.html"


class SignupDoneView(TemplateView):
    template_name = "main/signup_done.html"


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


class Settings(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = puser
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


def statistic(request):
    if request.method == 'POST':
        if 'add_data' in request.POST:
            form = ADForm(request.POST)
            if form.is_valid():
                listener = form.save(commit=False)
                if request.user.is_doctor:
                    listener.user = puser.objects.get(id=int(request.POST.getlist('add_type')[0]))
                else:
                    listener.user = request.user
                listener.type = TypeData.objects.get(id=request.POST.get("add_data"))
                listener.save()
                return redirect('/statistic')
        if 'add_type' in request.POST:
            form = TypeForm(request.POST)
            if form.is_valid():
                listener = form.save(commit=False)
                if request.user.is_doctor:
                    listener.user = puser.objects.get(id=int(request.POST.getlist('add_type')[0]))
                else:
                    listener.user = request.user
                listener.label = dict(form.choices)[form.cleaned_data["label"]]
                listener.save()
                return redirect('/statistic')
        if 'add_patient' in request.POST:
            form = AddPatientForm(request.POST)
            if form.is_valid():
                send_choice_notification(user=puser.objects.order_by().filter(email=form.cleaned_data.get("email"))[:1], username=request.user.username, email=form.cleaned_data.get("email"))
            return redirect('/statistic')
    FormAD = ADForm()
    FormType = TypeForm()
    if request.user.is_doctor:
        FormPatient = AddPatientForm()
        patients = puser.objects.order_by('-id').filter(user=request.user)
        types = TypeData.objects.order_by('-id')
        statistics = AD.objects.order_by('time')
        data = {
            'FormAD': FormAD,
            'FormType': FormType,
            'FormPatient': FormPatient,
            'patients': patients,
            'statistics': statistics,
            'type': types
        }
    else:
        types = TypeData.objects.order_by('-id').filter(user=request.user)
        statistics = AD.objects.order_by('time').filter(user=request.user)
        data = {
            'FormAD': FormAD,
            'FormType': FormType,
            'statistics': statistics,
            'type': types
        }
    return render(request, 'main/statistic.html', data)
