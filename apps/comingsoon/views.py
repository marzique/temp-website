from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError


def index(request):
    context = {}
    return render(request, 'comingsoon/index.html', context)
