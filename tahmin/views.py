from django.shortcuts import render, HttpResponse, get_object_or_404


def tahmin_home(request):
    return render(request, 'tahmin/tahminHome.html', {})