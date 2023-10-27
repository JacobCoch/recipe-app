from django.views.generic.detail import DetailView
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

class Profile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"