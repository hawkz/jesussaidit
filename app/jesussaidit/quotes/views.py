from django.views.generic import ListView, DetailView
from jesussaidit.quotes.models import Quote, Chapter


class AllQuotesView(ListView):
    queryset = Quote.objects.select_related().defer("chapter__content").all()
    allow_empty = False


class QuoteView(DetailView):
    queryset = Quote.objects.select_related().all()
    slug_field = 'slug'


class ChapterView(DetailView):
    model = Chapter
