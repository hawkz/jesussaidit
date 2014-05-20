from django.views.generic import ListView, DetailView
from jesussaidit.quotes.models import Quote, Chapter


class AllQuotesView(ListView):
    model = Quote
    allow_empty = False


class QuoteView(DetailView):
    model = Quote
    slug_field = 'slug'


class ChapterView(DetailView):
    model = Chapter
