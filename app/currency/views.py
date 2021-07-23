from currency.forms import RateForm
from currency.models import ContactUs, GoodCafe, Rate
from currency.utils import generate_password as gen_pass

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


def index(request):
    return render(request, 'index.html')


def generate_password(request):
    password_len = int(request.GET.get('password-len'))
    password = gen_pass(password_len)
    return HttpResponse(password)


def rate_list(request):
    rates = Rate.objects.all()
    context = {
        'rate_list': rates,
    }
    return render(request, 'rate_list.html', context=context)


def rate_create(request):  # スタンダードなフォームのテキスト
    if request.method == 'POST':
        form = RateForm(request.POST)  # 記入されたらフォーム内容を表示
        if form.is_valid():
            form.save()  # フォーム内容を保存
            return HttpResponseRedirect('/rate/list/')
    elif request.method == 'GET':
        form = RateForm()  # 最初は空白のフォーム
    context = {
        'form': form,
    }
    # breakpoint()
    return render(request, 'rate_create.html', context=context)


def rate_details(request, rate_id):
    rate = get_object_or_404(Rate, id=rate_id)
    context = {
        'object': rate,
    }
    return render(request, 'rate_details.html', context=context)


def rate_update(request, rate_id):
    rate = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        form = RateForm(request.POST, instance=rate)  # 元からinstanceの値rateを表示
        if form.is_valid():
            form.save()  # フォーム内容を保存
            return HttpResponseRedirect('/rate/list/')
    elif request.method == 'GET':
        form = RateForm(instance=rate)  # 元からinstanceの値rateを表示

    context = {
        'form': form,
    }
    return render(request, 'rate_update.html', context=context)


def rate_delete(request, rate_id):
    rate = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        rate.delete()
        return HttpResponseRedirect('/rate/list/')

    # if request.method == 'GET' #ここでは敢えて書く必要がない
    context = {
        'object': rate,
    }
    return render(request, 'rate_delete.html', context=context)


def contact_us_list(request):
    users = ContactUs.objects.all()
    context = {
        'contact_us_list': users,
    }
    return render(request, 'contact_us.html', context=context)


def good_cafe(request):
    cafes = GoodCafe.objects.all()
    context = {
        'good_cafe_list': cafes,
    }
    return render(request, 'good_cafe.html', context=context)


def response_codes(request):
    response = HttpResponse('Status code', status=301, headers={'Location': '/rate/list/'})
    return response
