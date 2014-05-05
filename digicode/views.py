from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def open_pasteur_gate(request):
    html = "<html><body>Door 'Pasteur' opened for 10 seconds.</body></html>" % now
    return HttpResponse(html)
