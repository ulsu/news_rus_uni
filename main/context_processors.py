from main.models import ActualInfo, NewsInfo, Newspaper


def actual(request):
    return {
        'active_side_actual': ActualInfo.objects.filter(display=True),
        'active_side_news': NewsInfo.objects.filter(display=True),
        }



def number(request):
    return {'header_number': Newspaper.objects.all().latest('date') if Newspaper.objects.all() else {}}