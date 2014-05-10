from django.views.generic import ListView, DetailView
from jesussaidit.quotes.models import Quote, Chapter
from django.shortcuts import get_object_or_404


class AllQuotesView(ListView):
    model = Quote


class QuoteView(DetailView):
    model = Quote
    slug_field = 'slug'


class ChapterView(DetailView):
    model = Chapter
