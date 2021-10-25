from currency.models import ContactUs


URL = '/currency/contact/us/create/'


def test_get_contactus(client):
    response = client.get(URL)
    assert response.status_code == 200


def test_post_empty_form(client):
    contactus_initial_count = ContactUs.objects.count()
    response = client.post(URL, data={})
    # if form is invalid, django returns status code 200
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'user_name': ['This field is required.'],
        'email_form': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.'],
    }
    assert ContactUs.objects.count() == contactus_initial_count


def test_invalid_form(client):
    contactus_initial_count = ContactUs.objects.count()
    form_data = {
        'user_name': 'Mr. Test',
        'email_form': 'test_invalid_formexamplecom',
        'subject': 'test_subject' * 100,
        'message': 'test_message',
    }
    response = client.post(URL, data=form_data)
    # if form is invalid, django returns status code 200
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email_form': ['Enter a valid email address.'],
        'subject': ['Ensure this value has at most 50 characters (it has 1200).'],
    }
    assert ContactUs.objects.count() == contactus_initial_count


def test_valid_form(client, mailoutbox):
    contactus_initial_count = ContactUs.objects.count()
    form_data = {
        'user_name': 'Mr. Test',
        'email_form': 'test_invalid_form@example.com',
        'subject': 'test_subject',
        'message': 'test_message',
    }
    response = client.post(URL, data=form_data)
    # if form is invalid, django returns status code 200
    assert response.status_code == 302
    assert response.url == '/'

    assert ContactUs.objects.count() == contactus_initial_count + 1
    contactus_object = ContactUs.objects.last()
    assert contactus_object.user_name == form_data['user_name']
    assert contactus_object.email_form == form_data['email_form']
    assert contactus_object.subject == form_data['subject']
    assert contactus_object.message == form_data['message']

    assert len(mailoutbox) == 1

    mail = mailoutbox[0]
    assert mail.to == ['python.test.yoshio@gmail.com']
    assert mail.from_email == 'python.test.yoshio@gmail.com'
