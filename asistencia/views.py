from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from .forms import UsuarioRegistroForm

class RegistroUsuarioView(CreateView):
    model =User
    form_class = UsuarioRegistroForm
    template_name ="registro.html"
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        user =form.save(commit=False)
        user.set_password(form. cleaned_data["password"])
        user.save()
        return super().form_valid(form)