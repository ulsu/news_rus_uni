from main.models import ActualInfo, Newspaper


def actual(request):
    return {'actual': ActualInfo.objects.filter(display=True)}

def number(request):
    return {'number': Newspaper.objects.latest('date')}