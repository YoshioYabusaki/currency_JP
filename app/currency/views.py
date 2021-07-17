from currency.models import ContactUs, Rate
from currency.utils import generate_password as gen_pass

from django.http import HttpResponse
from django.shortcuts import render


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


def contact_us_list(request):
    users = ContactUs.objects.all()
    context = {
        'contact_us_list': users,
    }
    return render(request, 'contact_us.html', context=context)


def response_codes(request):
    response = HttpResponse('Status code', status=301, headers={'Location': '/rate/list/'})
    return response
