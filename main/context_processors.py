from main.models import ActualInfo


def actual(request):
    return {'actual': ActualInfo.objects.filter(display=True)}