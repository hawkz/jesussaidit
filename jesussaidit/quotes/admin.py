from django.contrib import admin
from models import *


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'verse')
    list_filter = ['chapter__book', 'chapter__chapter']
    search_fields = ['quote']


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter')
    list_filter = ['book']
    search_fields = ['content']


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Chapter, ChapterAdmin)
