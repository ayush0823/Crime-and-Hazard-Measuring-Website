from .tasks import hourly_task
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def testcelery(request):
    hourly_task.delay()
    return HttpResponse("Test Successful")
