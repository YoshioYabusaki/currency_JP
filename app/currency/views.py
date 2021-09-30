from currency.forms import RateForm, SourceForm
from currency.models import ContactUs, GoodCafe, Rate, Source
from currency.tasks import contact_us
from currency.utils import generate_password as gen_pass

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
)


class GeneratePasswordView(TemplateView):
    template_name = 'generate_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        password_len = int(self.request.GET.get('password-len'))
        context['password'] = gen_pass(password_len)
        return context


class RateListView(ListView):  # ListView関数を使うと、以下簡単に書ける
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    # .select_related('source')はRateとSourceをJOINする
    template_name = 'rate_list.html'  # templatesフォルダにcurrencyフォルダ作り、このhtmlを入れれば本行書く必要なし。しかし。

    # ターミナルにCOOKIEを表示させる
    # def get(self, request, *args, **kwargs):
    #     print(request.COOKIES)
    #     return super().get(request, *args, **kwargs)


class RateCreateView(UserPassesTestMixin, CreateView):
    queryset = Rate.objects.all()
    form_class = RateForm  # クラスのように書くので()は必要ない
    success_url = reverse_lazy('currency:rate-list')  # 最初は見逃すけど次にリクエストがあったらやるよというlazy, Djangoではよくやる方法
    template_name = 'rate_create.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class RateDetailView(LoginRequiredMixin, DetailView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'


class RateUpdateView(UserPassesTestMixin, UpdateView):
    queryset = Rate.objects.all()
    form_class = RateForm  # クラスのように書くので()は必要ない
    success_url = reverse_lazy('currency:rate-list')  # 上手くいったら保存の上どこに移るか
    template_name = 'rate_update.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class RateDeleteView(UserPassesTestMixin, DeleteView):
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_delete.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


# CRUD операции для модели Source
class SourceListView(ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'


class SourceCreateView(UserPassesTestMixin, CreateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_create.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class SourceDetailView(LoginRequiredMixin, DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'


class SourceUpdateView(UserPassesTestMixin, UpdateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_update.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class SourceDeleteView(UserPassesTestMixin, DeleteView):
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_delete.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser


# модели ContactUs
class ContactUsListView(ListView):
    queryset = ContactUs.objects.all().order_by('-created')
    template_name = 'contact_us.html'


class ContactUsCreateView(CreateView):
    model = ContactUs
    success_url = reverse_lazy('index')
    template_name = 'contactus_create.html'
    fields = (
        'user_name',
        'email_form',
        'subject',
        'message',
    )  # フォームは自動生成される

    def form_valid(self, form):
        user_name = form.cleaned_data['user_name']
        email_form = form.cleaned_data['email_form']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        full_email_body = f'''
        User Name: {user_name}
        Email from: {email_form}
        Subject: {subject}
        Body: {message}
        '''
        contact_us.apply_async(args=(subject, ), kwargs={'body': full_email_body})

        return super().form_valid(form)


class GoodCafeListView(ListView):
    queryset = GoodCafe.objects.all()
    template_name = 'good_cafe.html'


# def rates_list_api_example(request):
#     import json
#     rates = Rate.objects.all()
#     result = []
#     for rate in rates:
#         result.append({
#             'id': rate.id,
#             'buy': float(rate.buy),
#             'sale': float(rate.sale),
#         })
#     # return HttpResponse(json.dumps(result), content_type='application/json')
#     return JsonResponse(result, safe=False)


def response_codes(request):
    response = HttpResponse('Status code', status=301, headers={'Location': '/rate/list/'})
    return response


# def rate_list(request):
#     rates = Rate.objects.all()
#     context = {
#         'rate_list': rates,
#     }
#     return render(request, 'rate_list.html', context=context)


# def rate_create(request):  # ↓スタンダードなフォームのテキスト
#     if request.method == 'POST':
#         form = RateForm(request.POST)  # 記入されたらフォーム内容を表示
#         if form.is_valid():
#             form.save()  # フォーム内容を保存
#             return HttpResponseRedirect('/rate/list/')
#     elif request.method == 'GET':
#         form = RateForm()  # 最初は空白のフォーム
#     context = {
#         'form': form,
#     }
#     # breakpoint()
#     return render(request, 'rate_create.html', context=context)


# def rate_details(request, rate_id):
#     rate = get_object_or_404(Rate, id=rate_id)
#     context = {
#         'object': rate,
#     }
#     return render(request, 'rate_details.html', context=context)


# def rate_update(request, rate_id):
#     rate = get_object_or_404(Rate, id=rate_id)
#
#     if request.method == 'POST':
#         form = RateForm(request.POST, instance=rate)  # 元からinstanceの値rateを表示
#         if form.is_valid():
#             form.save()  # フォーム内容を保存
#             return HttpResponseRedirect('/rate/list/')
#     elif request.method == 'GET':
#         form = RateForm(instance=rate)  # 元からinstanceの値rateを表示
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'rate_update.html', context=context)


# def rate_delete(request, rate_id):
#     rate = get_object_or_404(Rate, id=rate_id)
#
#     if request.method == 'POST':
#         rate.delete()
#         return HttpResponseRedirect('/rate/list/')
#     # if request.method == 'GET' #ここでは敢えて書く必要がない
#     context = {
#         'object': rate,
#     }
#     return render(request, 'rate_delete.html', context=context)


# def index(request):
#     return render(request, 'index.html')


# def generate_password(request):
#     password_len = int(request.GET.get('password-len'))
#     password = gen_pass(password_len)
#     return HttpResponse(password)


# def source_list(request):
#     source = Source.objects.all()
#     context = {
#         'source_list': source,
#     }
#     return render(request, 'source_list.html', context=context)


# def source_create(request):
#     if request.method == 'POST':  # サーバにデータを送る
#         form = SourceForm(request.POST)  # フォームのオブジェクトを作り、コンテクストに送る↓
#         if form.is_valid():  # フォーム内容を検証する
#             form.save()  # フォーム内容を保存
#             return HttpResponseRedirect('/source/list/')
#     elif request.method == 'GET':  # サーバからデータを得る
#         form = SourceForm()  # 最初は空白のフォーム
#     context = {
#         'form': form,
#     }
#     return render(request, 'source_create.html', context=context)  # templateに送る


# def source_details(request, source_id):
#     # try:
#     #     source = Source.objects.get(id=source_id)  # DBからひとつのオブジェクトを取り出す
#     # except Source.DoesNotExist as exc:
#     #     raise Http404(exc)
#     source = get_object_or_404(Source, id=source_id)  # 上記4行と全く同じ機能
#     context = {
#         'object': source,
#     }
#     return render(request, 'source_details.html', context=context)


# def source_update(request, source_id):  # フォームとオブジェクトを融合させる
#     source = get_object_or_404(Source, id=source_id)  # オブジェクトを得て
#
#     if request.method == 'POST':  # サーバにデータを送る
#         form = SourceForm(request.POST, instance=source)  # 元から値が入っているように
#         if form.is_valid():  # フォーム内容を検証する
#             form.save()  # フォーム内容を保存
#             return HttpResponseRedirect('/source/list/')
#     elif request.method == 'GET':  # サーバからデータを得る
#         form = SourceForm(instance=source)  # 元から値が入っているように
#     context = {
#         'form': form,
#     }
#     return render(request, 'source_update.html', context=context)


# def source_delete(request, source_id):
#     source = get_object_or_404(Source, id=source_id)
#
#     if request.method == 'POST':
#         source.delete()
#         return HttpResponseRedirect('/source/list/')
#     context = {
#         'object': source,
#     }
#     return render(request, 'source_delete.html', context=context)


# def contact_us_list(request):
#     users = ContactUs.objects.all()  # ここで得たデータを、
#     context = {  # 辞書型に変換し、下のrenderでhtmlに渡す
#         'contact_us_list': users,
#     }
#     return render(request, 'contact_us.html', context=context)


# def good_cafe(request):
#     cafes = GoodCafe.objects.all()
#     context = {
#         'good_cafe_list': cafes,
#     }
#     return render(request, 'good_cafe.html', context=context)
