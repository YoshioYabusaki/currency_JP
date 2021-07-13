from currency.models import ContactUs, Rate
from currency.utils import generate_password as gen_pass

from django.http import HttpResponse


def hello_world(request):
    return HttpResponse('Hello World')


def generate_password(request):
    password_len = int(request.GET.get('password-len'))
    password = gen_pass(password_len)
    return HttpResponse(password)


def rate_list(requests):
    rates = Rate.objects.all()

    result = []
    for rate in rates:
        # breakpoint()
        result.append(f'Id: {rate.id} Sale:{rate.sale} Buy:{rate.buy}</br>')

    return HttpResponse(str(result))


def contact_us_list(requests):
    users = ContactUs.objects.all()

    result = []
    for user in users:
        result.append(f'Id: {user.id} '
                      f'UserName:{user.user_name} '
                      f'Email:{user.email_form} '
                      f'Subject:{user.subject} '
                      f'Message:{user.message}</br>')

    return HttpResponse(str(result))
