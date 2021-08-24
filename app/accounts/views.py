from accounts.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class MyProfileView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = (
        'first_name',
        'last_name',
    )
    success_url = reverse_lazy('index')  # 上手くいったら保存の上どこに移るか
    template_name = 'my_profile.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(id=self.request.user.id)
    #     return queryset

    def get_object(self, queryset=None):
        return self.request.user
