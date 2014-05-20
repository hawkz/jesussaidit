from django.views.generic import ListView, DetailView
from jesussaidit.quotes.models import Quote, Chapter
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse


class AllQuotesView(ListView):
    queryset = Quote.objects.select_related().defer("chapter__content").all()
    allow_empty = False


def quote_view(request, book, chapter, verse):
    obj = get_object_or_404(Quote.objects.select_related().defer("chapter__content").all(),
                            chapter__slug=book,
                            chapter__chapter=chapter,
                            verse=verse
                            )

    return TemplateResponse(request, 'quotes/quote_detail.html', {
        'object': obj,
    })


def chapter_view(request, book, chapter):
    obj = get_object_or_404(Chapter.objects.all(),
                            slug=book,
                            chapter=chapter,
                            )

    return TemplateResponse(request, 'quotes/chapter_detail.html', {
        'object': obj,
    })
