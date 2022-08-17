from django.http import HttpResponse
from django.template import loader


def contact_page_view(request):
    template = loader.get_template('contact_page.html')
    return HttpResponse(template.render({}, request))

def contact_form_view(request):
    template