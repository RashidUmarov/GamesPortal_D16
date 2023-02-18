from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from .forms import MyUserProfile
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required

from board.models import Post, Author, Response


class UserProfile(LoginRequiredMixin, UpdateView):
    permission_required = ('allauth.change_user',)
    form_class = MyUserProfile
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        user = super().get_object()
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author__author=user).count()
        context['posts'] = posts

        responses = Response.objects.filter(post__author__author=user).count()
        context['responses'] = responses

        return context

    def get_success_url(self):  # new
        pk = self.kwargs["pk"]
        return reverse("profile", kwargs={"pk": pk})


@login_required
def subscribe(request):
    obj = Author.objects.get(author=request.user)
    obj.is_subscriber = True
    obj.save()
    return redirect('/', kwargs={"pk": request.user.pk})


@login_required
def unsubscribe(request):
    obj = Author.objects.get(author=request.user)
    obj.is_subscriber = False
    obj.save()
    return redirect('/', kwargs={"pk": request.user.pk})
