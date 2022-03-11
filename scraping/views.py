from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def index(request):
    form = FindForm()
    return render(request, 'scraping/index.html', {'form': form})


def list_view(request):
    form = FindForm()

    city = request.GET.get('city')
    language = request.GET.get('language')

    page_obj = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancies = Vacancy.objects.filter(**_filter)

        # пагинация
        paginator = Paginator(vacancies, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'object_list': page_obj,
        'form': form,
        'city': city,
        'language': language
    }
    return render(request, 'scraping/list.html', context)
