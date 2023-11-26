from django.http import HttpResponse
from django.shortcuts import render


def handler_404(request, exception):
    return render(request, 'pages/404.html', status=404)
