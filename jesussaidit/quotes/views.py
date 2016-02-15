from django.views.generic import ListView
from jesussaidit.quotes.models import Quote, Chapter
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import generic_search
from django.shortcuts import render_to_response

QUERY = "q"
MODEL_MAP = {Quote: ["quote", ]}


def search(request):
    objects = []

    if request.GET.get(QUERY, "").strip():

        for model, fields in MODEL_MAP.iteritems():
            objects += generic_search(request, model, fields, QUERY)

    paginator = Paginator(objects, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)

    return render_to_response("quotes/search_results.html",
                              {'object_list': object_list,
                               'img': 'img/jesus{r}.png'.format(r=randint(1, 30)),
                               'search_string': request.GET.get(QUERY, ""), })


class AllQuotesView(ListView):
    queryset = Quote.objects.select_related().defer("chapter__content").all()
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(AllQuotesView, self).get_context_data(**kwargs)
        context['img'] = 'img/jesus{r}.png'.format(r=randint(1, 30))
        return context


def quote_view(request, book, chapter, verse):
    obj = get_object_or_404(Quote.objects.select_related().defer("chapter__content").all(),
                            chapter__slug=book,
                            chapter__chapter=chapter,
                            verse=verse
                            )

    return TemplateResponse(request, 'quotes/quote_detail.html', {
        'object': obj,
        'img': 'img/jesus{r}.png'.format(r=randint(1, 30)),
    })


def chapter_view(request, book, chapter):
    obj = get_object_or_404(Chapter.objects.all(),
                            slug=book,
                            chapter=chapter,
                            )

    return TemplateResponse(request, 'quotes/chapter_detail.html', {
        'object': obj,
        'img': 'img/jesus{r}.png'.format(r=randint(1, 30)),
    })
